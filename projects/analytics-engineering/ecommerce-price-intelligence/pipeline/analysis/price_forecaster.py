"""
Price Forecasting using Prophet
"""
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logging.warning("Prophet not available. Install with: pip install prophet")

logger = logging.getLogger(__name__)


class PriceForecaster:
    """Forecast future prices using Facebook Prophet"""
    
    def __init__(self):
        self.model = None
        
        if not PROPHET_AVAILABLE:
            logger.warning("Prophet not installed. Forecasting disabled.")
    
    def prepare_data(self, price_history: List[Dict]) -> pd.DataFrame:
        """
        Prepare price history data for Prophet
        
        Args:
            price_history: List of dicts with 'date' and 'price' keys
            
        Returns:
            DataFrame with 'ds' and 'y' columns
        """
        df = pd.DataFrame(price_history)
        
        # Prophet requires 'ds' (date) and 'y' (value) columns
        df = df.rename(columns={'date': 'ds', 'price': 'y'})
        df['ds'] = pd.to_datetime(df['ds'])
        
        return df[['ds', 'y']]
    
    def train_model(self, price_data: pd.DataFrame) -> bool:
        """Train Prophet model on price data"""
        if not PROPHET_AVAILABLE:
            return False
        
        if len(price_data) < 10:
            logger.warning("Insufficient data for forecasting (need at least 10 points)")
            return False
        
        try:
            self.model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=False,
                changepoint_prior_scale=0.05,
                interval_width=0.95,
            )
            
            self.model.fit(price_data)
            logger.info("Model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
    
    def forecast(self, periods: int = 30) -> pd.DataFrame:
        """
        Generate forecast for future periods
        
        Args:
            periods: Number of days to forecast
            
        Returns:
            DataFrame with forecast
        """
        if not self.model:
            logger.error("Model not trained")
            return None
        
        try:
            future = self.model.make_future_dataframe(periods=periods)
            forecast = self.model.predict(future)
            
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            
        except Exception as e:
            logger.error(f"Error generating forecast: {e}")
            return None
    
    def forecast_product_price(self, price_history: List[Dict], 
                              forecast_days: int = 30) -> Dict:
        """
        Forecast price for a product
        
        Args:
            price_history: List of price records
            forecast_days: Days to forecast
            
        Returns:
            Dict with forecast results
        """
        if not PROPHET_AVAILABLE:
            return {'error': 'Prophet not available'}
        
        # Prepare data
        df = self.prepare_data(price_history)
        
        if len(df) < 10:
            return {'error': 'Insufficient historical data'}
        
        # Train model
        success = self.train_model(df)
        if not success:
            return {'error': 'Failed to train model'}
        
        # Generate forecast
        forecast_df = self.forecast(periods=forecast_days)
        
        if forecast_df is None:
            return {'error': 'Failed to generate forecast'}
        
        # Extract future forecasts
        future_forecast = forecast_df.tail(forecast_days)
        
        forecasts = []
        for _, row in future_forecast.iterrows():
            forecasts.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted_price': round(float(row['yhat']), 2),
                'lower_bound': round(float(row['yhat_lower']), 2),
                'upper_bound': round(float(row['yhat_upper']), 2),
            })
        
        # Summary statistics
        current_price = price_history[-1]['price']
        avg_forecast = future_forecast['yhat'].mean()
        price_trend = 'increasing' if avg_forecast > current_price else 'decreasing'
        
        return {
            'forecasts': forecasts,
            'current_price': current_price,
            'avg_forecast_price': round(float(avg_forecast), 2),
            'price_trend': price_trend,
            'forecast_days': forecast_days,
            'historical_points': len(df),
        }
    
    def find_best_buy_time(self, forecast_results: Dict) -> Dict:
        """Find the best time to buy based on forecast"""
        if 'error' in forecast_results:
            return {'error': forecast_results['error']}
        
        forecasts = forecast_results['forecasts']
        
        # Find date with minimum predicted price
        min_forecast = min(forecasts, key=lambda x: x['predicted_price'])
        
        # Calculate potential savings
        current_price = forecast_results['current_price']
        min_price = min_forecast['predicted_price']
        savings = current_price - min_price
        savings_percent = (savings / current_price) * 100
        
        recommendation = {
            'best_buy_date': min_forecast['date'],
            'predicted_price': min_price,
            'current_price': current_price,
            'potential_savings': round(savings, 2),
            'savings_percent': round(savings_percent, 2),
        }
        
        # Add recommendation text
        if savings_percent > 5:
            recommendation['action'] = 'wait'
            recommendation['message'] = f"Wait until {min_forecast['date']} to save {savings_percent:.1f}%"
        else:
            recommendation['action'] = 'buy_now'
            recommendation['message'] = "Price relatively stable. Buy now if needed."
        
        return recommendation





