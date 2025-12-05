"""
Sistema Híbrido de Recolección de Datos Financieros
Combina Yahoo Finance + Alpha Vantage para máxima cobertura
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
from time import sleep
from datetime import datetime
import os
import sys

# Importar configuración
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.api_keys import ALPHA_VANTAGE_KEY, ALPHA_VANTAGE_DAILY_LIMIT, ALPHA_VANTAGE_CALLS_PER_MINUTE


class HybridDataCollector:
    """
    Recolector híbrido que maximiza la cobertura de datos usando:
    1. Yahoo Finance (base, gratis, ilimitado)
    2. Alpha Vantage (complemento, 500 calls/día gratis)
    """
    
    def __init__(self, alpha_vantage_key=None, use_hybrid=True):
        self.av_key = alpha_vantage_key or ALPHA_VANTAGE_KEY
        self.use_hybrid = use_hybrid
        self.av_calls_today = 0
        self.av_limit = ALPHA_VANTAGE_DAILY_LIMIT
        self.errors = []
        
        print(f"🚀 HybridDataCollector inicializado")
        print(f"   Modo: {'Híbrido (Yahoo + Alpha Vantage)' if use_hybrid else 'Solo Yahoo Finance'}")
        if use_hybrid and self.av_key == "demo":
            print(f"   ⚠️  Usando API key demo - obtén la tuya en https://www.alphavantage.co/support/#api-key")
    
    # ===== YAHOO FINANCE =====
    
    def get_yahoo_market_data(self, ticker, start="2016-01-01", end="2023-12-31"):
        """Obtener datos de mercado (precios diarios) de Yahoo Finance"""
        try:
            empresa = yf.Ticker(ticker)
            historia = empresa.history(start=start, end=end)
            
            if historia.empty:
                print(f"⚠️ No se encontraron datos de mercado para {ticker}")
                return None
            
            historia.reset_index(inplace=True)
            print(f"✅ Datos de mercado Yahoo: {len(historia)} días")
            return historia
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de mercado Yahoo para {ticker}: {e}")
            self.errors.append({'ticker': ticker, 'source': 'yahoo_market', 'error': str(e)})
            return None
    
    def get_yahoo_financials(self, ticker):
        """Obtener datos financieros de Yahoo Finance"""
        try:
            empresa = yf.Ticker(ticker)
            
            # Balance Sheet
            balance = empresa.balance_sheet.T if hasattr(empresa, 'balance_sheet') else pd.DataFrame()
            
            # Income Statement
            income = empresa.financials.T if hasattr(empresa, 'financials') else pd.DataFrame()
            
            # Cash Flow
            cashflow = empresa.cashflow.T if hasattr(empresa, 'cashflow') else pd.DataFrame()
            
            if balance.empty and income.empty and cashflow.empty:
                print(f"⚠️ No se encontraron datos financieros para {ticker}")
                return None
            
            # Unir todos los datos
            datos_financieros = balance.join([income, cashflow], how='outer')
            datos_financieros.index.name = "Date"
            datos_financieros.reset_index(inplace=True)
            
            print(f"✅ Datos financieros Yahoo: {len(datos_financieros)} reportes")
            print(f"   Columnas disponibles: {len(datos_financieros.columns)}")
            
            return datos_financieros
            
        except Exception as e:
            print(f"❌ Error obteniendo datos financieros Yahoo para {ticker}: {e}")
            self.errors.append({'ticker': ticker, 'source': 'yahoo_financials', 'error': str(e)})
            return None
    
    def get_yahoo_shares_outstanding(self, ticker):
        """Obtener shares outstanding históricos de Yahoo"""
        try:
            empresa = yf.Ticker(ticker)
            balance = empresa.balance_sheet.T
            
            if 'Ordinary Shares Number' in balance.columns:
                shares = balance[['Ordinary Shares Number']].copy()
                shares.index = pd.to_datetime(shares.index)
                shares.columns = ['shares_outstanding']
                print(f"✅ Shares outstanding: {len(shares)} observaciones")
                return shares
            else:
                # Fallback: usar valor actual
                info = empresa.info
                shares_current = info.get('sharesOutstanding', None)
                if shares_current:
                    print(f"⚠️ Usando shares outstanding actual: {shares_current:,.0f}")
                    return pd.DataFrame({'shares_outstanding': [shares_current]}, 
                                       index=[pd.Timestamp.now()])
                else:
                    print(f"⚠️ No se encontraron shares outstanding para {ticker}")
                    return None
                
        except Exception as e:
            print(f"⚠️ Error obteniendo shares: {e}")
            return None
    
    # ===== ALPHA VANTAGE =====
    
    def get_alpha_vantage_income(self, ticker):
        """Obtener Income Statement de Alpha Vantage"""
        if not self.use_hybrid or self.av_calls_today >= self.av_limit:
            return None
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'INCOME_STATEMENT',
                'symbol': ticker,
                'apikey': self.av_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            self.av_calls_today += 1
            print(f"📊 Alpha Vantage call #{self.av_calls_today}/{self.av_limit}")
            
            # Rate limiting (5 calls/min gratis)
            if self.av_calls_today % ALPHA_VANTAGE_CALLS_PER_MINUTE == 0:
                print("⏳ Esperando 60s (límite de rate)...")
                sleep(60)
            else:
                sleep(12)  # 12s entre llamadas = 5 calls/min
            
            if 'annualReports' in data:
                df = pd.DataFrame(data['annualReports'])
                print(f"✅ Income Statement AV: {len(df)} reportes")
                return df
            else:
                print(f"⚠️ No hay datos de Income Statement en Alpha Vantage")
                return None
                
        except Exception as e:
            print(f"❌ Error Alpha Vantage Income: {e}")
            self.errors.append({'ticker': ticker, 'source': 'av_income', 'error': str(e)})
            return None
    
    def get_alpha_vantage_balance(self, ticker):
        """Obtener Balance Sheet de Alpha Vantage"""
        if not self.use_hybrid or self.av_calls_today >= self.av_limit:
            return None
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'BALANCE_SHEET',
                'symbol': ticker,
                'apikey': self.av_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            self.av_calls_today += 1
            print(f"📊 Alpha Vantage call #{self.av_calls_today}/{self.av_limit}")
            
            if self.av_calls_today % ALPHA_VANTAGE_CALLS_PER_MINUTE == 0:
                print("⏳ Esperando 60s (límite de rate)...")
                sleep(60)
            else:
                sleep(12)
            
            if 'annualReports' in data:
                df = pd.DataFrame(data['annualReports'])
                print(f"✅ Balance Sheet AV: {len(df)} reportes")
                return df
            else:
                print(f"⚠️ No hay datos de Balance Sheet en Alpha Vantage")
                return None
                
        except Exception as e:
            print(f"❌ Error Alpha Vantage Balance: {e}")
            self.errors.append({'ticker': ticker, 'source': 'av_balance', 'error': str(e)})
            return None
    
    def get_alpha_vantage_cashflow(self, ticker):
        """Obtener Cash Flow de Alpha Vantage"""
        if not self.use_hybrid or self.av_calls_today >= self.av_limit:
            return None
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'CASH_FLOW',
                'symbol': ticker,
                'apikey': self.av_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            self.av_calls_today += 1
            print(f"📊 Alpha Vantage call #{self.av_calls_today}/{self.av_limit}")
            
            if self.av_calls_today % ALPHA_VANTAGE_CALLS_PER_MINUTE == 0:
                print("⏳ Esperando 60s (límite de rate)...")
                sleep(60)
            else:
                sleep(12)
            
            if 'annualReports' in data:
                df = pd.DataFrame(data['annualReports'])
                print(f"✅ Cash Flow AV: {len(df)} reportes")
                return df
            else:
                print(f"⚠️ No hay datos de Cash Flow en Alpha Vantage")
                return None
                
        except Exception as e:
            print(f"❌ Error Alpha Vantage CashFlow: {e}")
            self.errors.append({'ticker': ticker, 'source': 'av_cashflow', 'error': str(e)})
            return None
    
    # ===== MÉTODOS PRINCIPALES =====
    
    def check_data_completeness(self, df_financials, critical_items):
        """Verifica qué datos críticos faltan en Yahoo"""
        if df_financials is None:
            return critical_items
        
        missing = []
        for item in critical_items:
            if item not in df_financials.columns:
                missing.append(item)
        
        return missing
    
    def collect_company_data(self, ticker, start="2016-01-01", end="2023-12-31"):
        """
        Recolecta TODOS los datos de una empresa usando estrategia híbrida
        """
        print(f"\n{'='*60}")
        print(f"🏢 Recolectando datos para {ticker}")
        print(f"{'='*60}")
        
        result = {
            'ticker': ticker,
            'timestamp': datetime.now(),
            'market_data': None,
            'financial_data': None,
            'shares_outstanding': None,
            'alpha_vantage_supplement': {},
            'data_quality': {},
            'errors': []
        }
        
        # 1. DATOS DE MERCADO (Yahoo - siempre primero)
        print("\n📈 Paso 1/4: Datos de Mercado")
        result['market_data'] = self.get_yahoo_market_data(ticker, start, end)
        
        # 2. DATOS FINANCIEROS (Yahoo)
        print("\n📊 Paso 2/4: Datos Financieros")
        result['financial_data'] = self.get_yahoo_financials(ticker)
        
        # 3. SHARES OUTSTANDING (Yahoo)
        print("\n🔢 Paso 3/4: Shares Outstanding")
        result['shares_outstanding'] = self.get_yahoo_shares_outstanding(ticker)
        
        # 4. COMPLEMENTAR CON ALPHA VANTAGE (si hay gaps)
        print("\n🔍 Paso 4/4: Verificando completitud de datos")
        
        if result['financial_data'] is not None:
            critical_items = [
                'Total Revenue', 'Cost Of Revenue', 'EBIT', 'Net Income',
                'Total Assets', 'Total Liabilities Net Minority Interest',
                'Stockholders Equity', 'Capital Expenditure', 'Operating Cash Flow'
            ]
            
            missing = self.check_data_completeness(result['financial_data'], critical_items)
            
            if missing and self.use_hybrid:
                print(f"⚠️ Faltan {len(missing)} items críticos en Yahoo:")
                for item in missing[:5]:  # Mostrar solo primeros 5
                    print(f"   - {item}")
                
                print(f"\n🔄 Complementando con Alpha Vantage...")
                
                # Obtener datos de AV
                av_income = self.get_alpha_vantage_income(ticker)
                av_balance = self.get_alpha_vantage_balance(ticker)
                av_cashflow = self.get_alpha_vantage_cashflow(ticker)
                
                result['alpha_vantage_supplement'] = {
                    'income': av_income,
                    'balance': av_balance,
                    'cashflow': av_cashflow
                }
            elif missing:
                print(f"⚠️ Faltan {len(missing)} items pero modo híbrido desactivado")
            else:
                print(f"✅ Todos los items críticos están presentes en Yahoo")
        
        # Calcular métricas de calidad
        result['data_quality'] = self._calculate_data_quality(result)
        
        print(f"\n{'='*60}")
        print(f"✅ Recolección completada para {ticker}")
        print(f"   Calidad de datos: {result['data_quality']['overall_score']:.1f}%")
        print(f"{'='*60}")
        
        return result
    
    def _calculate_data_quality(self, result):
        """Calcula métricas de calidad de los datos recolectados"""
        quality = {
            'has_market_data': result['market_data'] is not None,
            'has_financial_data': result['financial_data'] is not None,
            'has_shares': result['shares_outstanding'] is not None,
            'av_supplemented': len(result['alpha_vantage_supplement']) > 0,
            'overall_score': 0
        }
        
        # Calcular score general
        score = 0
        if quality['has_market_data']: score += 40
        if quality['has_financial_data']: score += 40
        if quality['has_shares']: score += 10
        if quality['av_supplemented']: score += 10
        
        quality['overall_score'] = score
        
        return quality
    
    def save_data(self, result, output_dir="../data/raw"):
        """Guarda los datos recolectados"""
        os.makedirs(output_dir, exist_ok=True)
        ticker = result['ticker']
        
        # Guardar datos de mercado
        if result['market_data'] is not None:
            market_path = f"{output_dir}/{ticker}_market_data.csv"
            result['market_data'].to_csv(market_path, index=False)
            print(f"💾 Guardado: {market_path}")
        
        # Guardar datos financieros
        if result['financial_data'] is not None:
            financial_path = f"{output_dir}/{ticker}_financial_data.csv"
            result['financial_data'].to_csv(financial_path, index=False)
            print(f"💾 Guardado: {financial_path}")
        
        # Guardar datos de Alpha Vantage (si existen)
        if result['alpha_vantage_supplement']:
            for key, df in result['alpha_vantage_supplement'].items():
                if df is not None:
                    av_path = f"{output_dir}/{ticker}_av_{key}.csv"
                    df.to_csv(av_path, index=False)
                    print(f"💾 Guardado: {av_path}")
        
        # Guardar reporte de calidad
        quality_path = f"{output_dir}/{ticker}_quality_report.txt"
        with open(quality_path, 'w') as f:
            f.write(f"Reporte de Calidad - {ticker}\n")
            f.write(f"Generado: {result['timestamp']}\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Datos de Mercado: {'✅' if result['data_quality']['has_market_data'] else '❌'}\n")
            f.write(f"Datos Financieros: {'✅' if result['data_quality']['has_financial_data'] else '❌'}\n")
            f.write(f"Shares Outstanding: {'✅' if result['data_quality']['has_shares'] else '❌'}\n")
            f.write(f"Suplemento Alpha Vantage: {'✅' if result['data_quality']['av_supplemented'] else '❌'}\n")
            f.write(f"\nScore General: {result['data_quality']['overall_score']:.1f}%\n")
        
        print(f"💾 Guardado: {quality_path}")


# ===== FUNCIÓN DE AYUDA =====

def collect_single_company(ticker, use_hybrid=True, alpha_vantage_key=None):
    """Función helper para recolectar datos de una sola empresa"""
    collector = HybridDataCollector(
        alpha_vantage_key=alpha_vantage_key,
        use_hybrid=use_hybrid
    )
    
    result = collector.collect_company_data(ticker)
    collector.save_data(result)
    
    return result


if __name__ == "__main__":
    # Test rápido
    print("🧪 Modo de prueba - recolectando datos de AAPL")
    result = collect_single_company("AAPL", use_hybrid=False)  # Solo Yahoo para prueba
    print(f"\n✅ Prueba completada. Score de calidad: {result['data_quality']['overall_score']}%")