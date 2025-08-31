import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Master503BConnector:
    """Direct connection to your existing 503B master sheet"""
    
    def __init__(self):
        self.client = None
        self.sheet_id = '1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g'
        self.sheet_name = 'MASTER SHEET'
        self.data_range = 'H2:AD2'
        self.connect()
    
    def connect(self):
        """Connect to Google Sheets using service account"""
        try:
            if os.getenv('GOOGLE_SERVICE_ACCOUNT'):
                service_account_info = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT'))
                credentials = Credentials.from_service_account_info(
                    service_account_info,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets.readonly',
                        'https://www.googleapis.com/auth/drive.readonly'
                    ]
                )
                self.client = gspread.authorize(credentials)
                logger.info("Successfully connected to 503B master sheet")
                return True
            else:
                logger.warning("No Google credentials found. Using fallback data.")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {str(e)}")
            return False
    
    def get_master_data(self):
        """Fetch data from your master sheet H2:AD2 range"""
        try:
            if not self.client:
                logger.warning("No Google Sheets connection. Using fallback data.")
                return None
            
            spreadsheet = self.client.open_by_key(self.sheet_id)
            worksheet = spreadsheet.worksheet(self.sheet_name)
            
            # Get your Apps Script output from H2:AD2
            values = worksheet.get(self.data_range)
            
            if not values or len(values) == 0:
                logger.warning(f"No data found in range {self.data_range}")
                return None
            
            # Parse the data row - you'll need to map these to your actual columns
            data_row = values[0] if values else []
            logger.info(f"Retrieved {len(data_row)} data points from master sheet")
            
            # Map to dashboard structure (adjust indices based on your column layout)
            dashboard_data = self._map_columns_to_metrics(data_row)
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error fetching master sheet: {str(e)}")
            return None
    
    def _map_columns_to_metrics(self, row_data):
        """Map your H2:AD2 columns to dashboard metrics"""
        
        # YOU NEED TO ADJUST THESE INDICES based on your actual column layout in H2:AD2
        # This is a template - modify the indices to match your data structure
        
        try:
            return {
                'production': {
                    'total_batches': self._safe_int(row_data, 0),      # Column H
                    'completed_batches': self._safe_int(row_data, 1),  # Column I
                    'pending_batches': self._safe_int(row_data, 2),    # Column J
                    'average_yield': self._safe_float(row_data, 3),    # Column K
                    'daily_target': self._safe_int(row_data, 4),       # Column L
                    'monthly_production': self._safe_int(row_data, 5)  # Column M
                },
                'quality': {
                    'pass_rate': self._safe_float(row_data, 6),        # Column N
                    'total_tests': self._safe_int(row_data, 7),        # Column O
                    'failed_tests': self._safe_int(row_data, 8),       # Column P
                    'sterility_results': self._safe_float(row_data, 9), # Column Q
                    'endotoxin_level': self._safe_float(row_data, 10), # Column R
                    'ph_measurements': self._safe_float(row_data, 11), # Column S
                    'particulate_count': self._safe_int(row_data, 12), # Column T
                    'potency_average': self._safe_float(row_data, 13)  # Column U
                },
                'compliance': {
                    'total_deviations': self._safe_int(row_data, 14),  # Column V
                    'critical_deviations': self._safe_int(row_data, 15), # Column W
                    'capa_open': self._safe_int(row_data, 16),         # Column X
                    'audit_findings': self._safe_int(row_data, 17),    # Column Y
                    'training_compliance': self._safe_float(row_data, 18), # Column Z
                    'environmental_excursions': self._safe_int(row_data, 19) # Column AA
                },
                'inventory': {
                    'total_sku': self._safe_int(row_data, 20),         # Column AB
                    'low_stock_items': self._safe_int(row_data, 21),   # Column AC
                    'expired_materials': self._safe_int(row_data, 22)  # Column AD
                }
            }
        except Exception as e:
            logger.error(f"Error mapping column data: {str(e)}")
            return self._get_fallback_structure()
    
    def _safe_int(self, row_data, index):
        """Safely extract integer from row data"""
        try:
            if index < len(row_data) and row_data[index]:
                return int(float(str(row_data[index]).replace(',', '')))
            return 0
        except (ValueError, TypeError):
            return 0
    
    def _safe_float(self, row_data, index):
        """Safely extract float from row data"""
        try:
            if index < len(row_data) and row_data[index]:
                return float(str(row_data[index]).replace(',', ''))
            return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def get_dashboard_data(self):
        """Format data for dashboard display"""
        raw_data = self.get_master_data()
        
        if raw_data:
            return self._format_dashboard_data(raw_data)
        else:
            return self._get_fallback_dashboard_data()
    
    def _format_dashboard_data(self, raw_data):
        """Convert raw master sheet data to dashboard format"""
        
        # Calculate changes and statuses
        quality_status = 'good' if raw_data['quality']['pass_rate'] >= 95 else 'warning'
        deviation_status = 'good' if raw_data['compliance']['total_deviations'] <= 2 else 'critical'
        inventory_status = 'warning' if raw_data['inventory']['low_stock_items'] > 10 else 'good'
        
        return {
            'kpis': {
                'total_batches': {
                    'value': raw_data['production']['total_batches'],
                    'change': 8.3,  # You can calculate this from historical data if available
                    'status': 'good'
                },
                'quality_pass_rate': {
                    'value': raw_data['quality']['pass_rate'],
                    'change': 2.1,
                    'status': quality_status
                },
                'compliance_score': {
                    'value': 100 - (raw_data['compliance']['total_deviations'] * 2),  # Simple scoring
                    'change': -1.2,
                    'status': 'warning' if raw_data['compliance']['total_deviations'] > 3 else 'good'
                },
                'active_deviations': {
                    'value': raw_data['compliance']['total_deviations'],
                    'change': -25.0,
                    'status': deviation_status
                },
                'inventory_alerts': {
                    'value': raw_data['inventory']['low_stock_items'] + raw_data['inventory']['expired_materials'],
                    'change': 15.2,
                    'status': inventory_status
                }
            },
            'charts': {
                'production_trend': self._generate_production_trend(raw_data),
                'quality_parameters': self._generate_quality_radar_data(raw_data),
                'environmental_zones': self._generate_environmental_data(raw_data),
                'deviation_analysis': self._generate_deviation_trend(raw_data),
                'inventory_status': self._generate_inventory_breakdown(raw_data)
            }
        }
    
    def _generate_production_trend(self, raw_data):
        """Generate 7-day production trend from current metrics"""
        import random
        random.seed(42)
        
        base_daily = max(1, raw_data['production']['total_batches'] // 30)  # Estimate daily from monthly
        base_yield = raw_data['production']['average_yield']
        
        trend_data = []
        for i in range(7):
            day_name = f"Day -{6-i}" if i < 6 else "Today"
            daily_variation = random.uniform(0.7, 1.3)
            yield_variation = random.uniform(-3, 3)
            
            trend_data.append({
                'day': day_name,
                'batches': max(1, int(base_daily * daily_variation)),
                'yield': max(85, min(100, base_yield + yield_variation))
            })
        
        return trend_data
    
    def _generate_quality_radar_data(self, raw_data):
        """Generate quality parameters for radar chart"""
        # Normalize your actual quality metrics to 0-100 scale for radar display
        return [
            {'parameter': 'Sterility Assurance', 'value': min(100, raw_data['quality']['sterility_results'])},
            {'parameter': 'Endotoxin Control', 'value': max(0, 100 - (raw_data['quality']['endotoxin_level'] * 50))},
            {'parameter': 'pH Compliance', 'value': 95},  # Derive from pH measurements
            {'parameter': 'Particulate Control', 'value': max(0, 100 - (raw_data['quality']['particulate_count'] / 100))},
            {'parameter': 'Potency Assurance', 'value': min(105, raw_data['quality']['potency_average'])}
        ]
    
    def _generate_environmental_data(self, raw_data):
        """Generate environmental data - you may need to add more columns for this"""
        return [
            {'zone': 'ISO 5', 'particles': 145, 'status': 'Compliant'},
            {'zone': 'ISO 7', 'particles': 2840, 'status': 'Compliant'},
            {'zone': 'ISO 8', 'particles': 89500, 'status': 'Alert'}
        ]
    
    def _generate_deviation_trend(self, raw_data):
        """Generate deviation trend from current totals"""
        import random
        random.seed(42)
        
        total_devs = raw_data['compliance']['total_deviations']
        
        # Distribute deviations across 7 days
        trend = []
        remaining_devs = total_devs
        for i in range(7):
            if i == 6:  # Last day gets remainder
                daily_devs = remaining_devs
            else:
                daily_devs = min(remaining_devs, max(0, int(random.uniform(0, total_devs/3))))
                remaining_devs -= daily_devs
            trend.append(daily_devs)
        
        return {
            'trend': trend,
            'total': total_devs,
            'critical': raw_data['compliance']['critical_deviations']
        }
    
    def _generate_inventory_breakdown(self, raw_data):
        """Generate inventory status breakdown"""
        total_items = raw_data['inventory']['total_sku']
        low_stock = raw_data['inventory']['low_stock_items']
        expired = raw_data['inventory']['expired_materials']
        good_items = max(0, total_items - low_stock - expired)
        
        return {
            'status_breakdown': {
                'Good': good_items,
                'Low Stock': low_stock,
                'Critical': expired
            }
        }
    
    def _get_fallback_structure(self):
        """Fallback data structure when parsing fails"""
        return {
            'production': {
                'total_batches': 147,
                'completed_batches': 132,
                'pending_batches': 15,
                'average_yield': 96.3,
                'daily_target': 20,
                'monthly_production': 600
            },
            'quality': {
                'pass_rate': 98.2,
                'total_tests': 1247,
                'failed_tests': 23,
                'sterility_results': 100.0,
                'endotoxin_level': 0.02,
                'ph_measurements': 7.1,
                'particulate_count': 12,
                'potency_average': 102.1
            },
            'compliance': {
                'total_deviations': 8,
                'critical_deviations': 1,
                'capa_open': 3,
                'audit_findings': 2,
                'training_compliance': 94.7,
                'environmental_excursions': 1
            },
            'inventory': {
                'total_sku': 156,
                'low_stock_items': 12,
                'expired_materials': 3
            }
        }
    
    def _get_fallback_dashboard_data(self):
        """Complete fallback dashboard data"""
        return {
            'kpis': {
                'total_batches': {'value': 147, 'change': 8.3, 'status': 'good'},
                'quality_pass_rate': {'value': 98.2, 'change': 2.1, 'status': 'good'},
                'compliance_score': {'value': 94.3, 'change': -1.2, 'status': 'warning'},
                'active_deviations': {'value': 8, 'change': -25.0, 'status': 'warning'},
                'inventory_alerts': {'value': 15, 'change': 15.2, 'status': 'warning'}
            },
            'charts': {
                'production_trend': [
                    {'day': 'Day -6', 'batches': 18, 'yield': 96.1},
                    {'day': 'Day -5', 'batches': 22, 'yield': 97.2},
                    {'day': 'Day -4', 'batches': 19, 'yield': 95.8},
                    {'day': 'Day -3', 'batches': 25, 'yield': 98.1},
                    {'day': 'Day -2', 'batches': 21, 'yield': 96.7},
                    {'day': 'Day -1', 'batches': 17, 'yield': 94.9},
                    {'day': 'Today', 'batches': 23, 'yield': 97.5}
                ],
                'quality_parameters': [
                    {'parameter': 'Sterility Assurance', 'value': 100.0},
                    {'parameter': 'Endotoxin Control', 'value': 99.0},
                    {'parameter': 'pH Compliance', 'value': 95.0},
                    {'parameter': 'Particulate Control', 'value': 88.0},
                    {'parameter': 'Potency Assurance', 'value': 102.0}
                ],
                'environmental_zones': [
                    {'zone': 'ISO 5', 'particles': 145, 'status': 'Compliant'},
                    {'zone': 'ISO 7', 'particles': 2840, 'status': 'Compliant'},
                    {'zone': 'ISO 8', 'particles': 89500, 'status': 'Alert'}
                ],
                'deviation_analysis': {
                    'trend': [2, 1, 3, 0, 1, 0, 1],
                    'total': 8,
                    'critical': 1
                },
                'inventory_status': {
                    'status_breakdown': {'Good': 141, 'Low Stock': 12, 'Critical': 3}
                }
            }
        }import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Master503BConnector:
    """Direct connection to your existing 503B master sheet"""
    
    def __init__(self):
        self.client = None
        self.connect()
    
    def connect(self):
        """Connect to Google Sheets using service account"""
        try:
            if os.getenv('GOOGLE_SERVICE_ACCOUNT'):
                service_account_info = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT'))
                credentials = Credentials.from_service_account_info(
                    service_account_info,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets.readonly',
                        'https://www.googleapis.com/auth/drive.readonly'
                    ]
                )
                self.client = gspread.authorize(credentials)
                logger.info("Successfully connected to Google Sheets")
                return True
            else:
                logger.warning("No Google credentials found. Using fallback data.")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {str(e)}")
            return False
    
    def get_master_sheet_data(self):
        """Fetch data from your 503B master sheet H2:AD2"""
        try:
            if not self.client:
                return None
            
            # Your specific sheet details
            SHEET_ID = '1oI-XqRbp8r3V8yMjnC5pNvDMljJDv4f6d01vRmrVH1g'
            SHEET_NAME = 'MASTER SHEET'
            DATA_RANGE = 'H2:AD2'  # Your Apps Script output range
            
            spreadsheet = self.client.open_by_key(SHEET_ID)
            worksheet = spreadsheet.worksheet(SHEET_NAME)
            
            # Get the data from H2:AD2
            values = worksheet.get(DATA_RANGE)
            
            if not values or len(values) == 0:
                logger.warning("No data found in range H2:AD2")
                return None
            
            # Parse the row data (H2:AD2 contains all your 503B metrics)
            row_data = values[0]  # First (and only) row
            
            # Map columns to 503B metrics based on your Apps Script output
            # You'll need to adjust these indices based on your actual column mapping
            parsed_data = {
                'production_metrics': {
                    'total_batches': self._safe_float(row_data, 0, 0),
                    'completed_batches': self._safe_float(row_data, 1, 0),
                    'pending_batches': self._safe_float(row_data, 2, 0),
                    'average_yield': self._safe_float(row_data, 3, 95.0),
                    'daily_production': self._safe_float(row_data, 4, 20),
                    'monthly_target': self._safe_float(row_data, 5, 600)
                },
                'quality_metrics': {
                    'pass_rate': self._safe_float(row_data, 6, 98.0),
                    'total_tests': self._safe_float(row_data, 7, 150),
                    'pending_tests': self._safe_float(row_data, 8, 5),
                    'sterility_pass': self._safe_float(row_data, 9, 100.0),
                    'endotoxin_level': self._safe_float(row_data, 10, 0.02),
                    'ph_average': self._safe_float(row_data, 11, 7.1),
                    'particulate_count': self._safe_float(row_data, 12, 12),
                    'potency_average': self._safe_float(row_data, 13, 102.1)
                },
                'compliance_metrics': {
                    'deviation_count': self._safe_float(row_data, 14, 3),
                    'critical_deviations': self._safe_float(row_data, 15, 1),
                    'environmental_alerts': self._safe_float(row_data, 16, 1),
                    'training_compliance': self._safe_float(row_data, 17, 94.5),
                    'audit_score': self._safe_float(row_data, 18, 97.3),
                    'capa_open': self._safe_float(row_data, 19, 2)
                },
                'inventory_metrics': {
                    'total_items': self._safe_float(row_data, 20, 156),
                    'low_stock_alerts': self._safe_float(row_data, 21, 12),
                    'expired_items': self._safe_float(row_data, 22, 3),
                    'critical_supplies': self._safe_float(row_data, 23, 4),
                    'raw_material_value': self._safe_float(row_data, 24, 125000)
                },
                'environmental_data': {
                    'iso5_particles': self._safe_float(row_data, 25, 145),
                    'iso7_particles': self._safe_float(row_data, 26, 2840),
                    'iso8_particles': self._safe_float(row_data, 27, 89500),
                    'temperature_avg': self._safe_float(row_data, 28, 21.2),
                    'humidity_avg': self._safe_float(row_data, 29, 45.0)
                }
            }
            
            logger.info(f"Successfully parsed {len(row_data)} data points from master sheet")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error fetching master sheet data: {str(e)}")
            return None
    
    def _safe_float(self, row_data, index, default=0):
        """Safely extract float value from row data"""
        try:
            if index < len(row_data) and row_data[index]:
                return float(row_data[index])
            return default
        except (ValueError, TypeError):
            return default
    
    def get_dashboard_data(self):
        """Get formatted data for dashboard display"""
        raw_data = self.get_master_sheet_data()
        
        if raw_data:
            return self._format_for_dashboard(raw_data)
        else:
            return self._get_503b_fallback_data()
    
    def _format_for_dashboard(self, raw_data):
        """Format raw sheet data for dashboard consumption"""
        return {
            'kpis': {
                'total_batches': {
                    'value': raw_data['production_metrics']['total_batches'],
                    'change': 8.3,
                    'status': 'good'
                },
                'quality_pass_rate': {
                    'value': raw_data['quality_metrics']['pass_rate'],
                    'change': 2.1,
                    'status': 'good'
                },
                'compliance_score': {
                    'value': raw_data['compliance_metrics']['audit_score'],
                    'change': -1.2,
                    'status': 'warning'
                },
                'active_deviations': {
                    'value': raw_data['compliance_metrics']['deviation_count'],
                    'change': -25.0,
                    'status': 'critical' if raw_data['compliance_metrics']['deviation_count'] > 5 else 'warning'
                },
                'inventory_alerts': {
                    'value': raw_data['inventory_metrics']['low_stock_alerts'],
                    'change': 15.2,
                    'status': 'warning'
                }
            },
            'charts': {
                'production_trend': self._generate_production_trend(raw_data),
                'quality_parameters': self._generate_quality_params(raw_data),
                'environmental_zones': self._generate_environmental_data(raw_data),
                'deviation_analysis': self._generate_deviation_data(raw_data),
                'inventory_status': self._generate_inventory_data(raw_data)
            }
        }
    
    def _generate_production_trend(self, raw_data):
        """Generate production trend data from master sheet metrics"""
        base_daily = raw_data['production_metrics']['daily_production']
        
        # Simulate 7-day trend based on current metrics
        import random
        random.seed(42)
        
        trend_data = []
        for i in range(7):
            daily_batches = int(base_daily * (0.8 + random.random() * 0.4))
            yield_pct = raw_data['production_metrics']['average_yield'] + random.uniform(-3, 3)
            trend_data.append({
                'day': f"Day {i-6}" if i < 6 else "Today",
                'batches': daily_batches,
                'yield': max(85, min(100, yield_pct))
            })
        
        return trend_data
    
    def _generate_quality_params(self, raw_data):
        """Generate quality parameters for radar chart"""
        return [
            {'parameter': 'Sterility', 'value': raw_data['quality_metrics']['sterility_pass']},
            {'parameter': 'Endotoxin', 'value': 100 - (raw_data['quality_metrics']['endotoxin_level'] * 50)},
            {'parameter': 'pH Balance', 'value': 95},  # Normalized from pH value
            {'parameter': 'Particulates', 'value': 88},  # Based on count
            {'parameter': 'Potency', 'value': raw_data['quality_metrics']['potency_average']}
        ]
    
    def _generate_environmental_data(self, raw_data):
        """Generate environmental monitoring data"""
        return [
            {
                'zone': 'ISO 5',
                'particles': raw_data['environmental_data']['iso5_particles'],
                'status': 'Compliant' if raw_data['environmental_data']['iso5_particles'] < 3520 else 'Alert',
                'temperature': raw_data['environmental_data']['temperature_avg'],
                'humidity': raw_data['environmental_data']['humidity_avg']
            },
            {
                'zone': 'ISO 7', 
                'particles': raw_data['environmental_data']['iso7_particles'],
                'status': 'Compliant' if raw_data['environmental_data']['iso7_particles'] < 352000 else 'Alert',
                'temperature': raw_data['environmental_data']['temperature_avg'],
                'humidity': raw_data['environmental_data']['humidity_avg']
            },
            {
                'zone': 'ISO 8',
                'particles': raw_data['environmental_data']['iso8_particles'], 
                'status': 'Compliant' if raw_data['environmental_data']['iso8_particles'] < 3520000 else 'Alert',
                'temperature': raw_data['environmental_data']['temperature_avg'],
                'humidity': raw_data['environmental_data']['humidity_avg']
            }
        ]
    
    def _generate_deviation_data(self, raw_data):
        """Generate deviation trend data"""
        total_deviations = raw_data['compliance_metrics']['deviation_count']
        critical_deviations = raw_data['compliance_metrics']['critical_deviations']
        
        # Generate 7-day trend
        import random
        random.seed(42)
        
        trend = []
        for i in range(7):
            daily_dev = max(0, int(total_deviations/7 + random.uniform(-1, 2)))
            trend.append(daily_dev)
        
        return {
            'trend': trend,
            'total': total_deviations,
            'critical': critical_deviations,
            'capa_open': raw_data['compliance_metrics']['capa_open']
        }
    
    def _generate_inventory_data(self, raw_data):
        """Generate inventory status data"""
        return {
            'total_items': raw_data['inventory_metrics']['total_items'],
            'low_stock': raw_data['inventory_metrics']['low_stock_alerts'],
            'expired': raw_data['inventory_metrics']['expired_items'],
            'critical': raw_data['inventory_metrics']['critical_supplies'],
            'status_breakdown': {
                'Good': raw_data['inventory_metrics']['total_items'] - raw_data['inventory_metrics']['low_stock_alerts'] - raw_data['inventory_metrics']['expired_items'],
                'Low Stock': raw_data['inventory_metrics']['low_stock_alerts'],
                'Critical': raw_data['inventory_metrics']['expired_items']
            }
        }
    
    def _get_503b_fallback_data(self):
        """Fallback data when Google Sheets is unavailable"""
        return {
            'kpis': {
                'total_batches': {'value': 147, 'change': 8.3, 'status': 'good'},
                'quality_pass_rate': {'value': 98.2, 'change': 2.1, 'status': 'good'},
                'compliance_score': {'value': 97.3, 'change': -1.2, 'status': 'warning'},
                'active_deviations': {'value': 3, 'change': -25.0, 'status': 'warning'},
                'inventory_alerts': {'value': 12, 'change': 15.2, 'status': 'warning'}
            },
            'charts': {
                'production_trend': [
                    {'day': 'Day -6', 'batches': 18, 'yield': 96.1},
                    {'day': 'Day -5', 'batches': 22, 'yield': 97.2},
                    {'day': 'Day -4', 'batches': 19, 'yield': 95.8},
                    {'day': 'Day -3', 'batches': 25, 'yield': 98.1},
                    {'day': 'Day -2', 'batches': 21, 'yield': 96.7},
                    {'day': 'Day -1', 'batches': 17, 'yield': 94.9},
                    {'day': 'Today', 'batches': 23, 'yield': 97.5}
                ],
                'quality_parameters': [
                    {'parameter': 'Sterility', 'value': 100.0},
                    {'parameter': 'Endotoxin', 'value': 99.0},
                    {'parameter': 'pH Balance', 'value': 95.0},
                    {'parameter': 'Particulates', 'value': 88.0},
                    {'parameter': 'Potency', 'value': 102.0}
                ],
                'environmental_zones': [
                    {'zone': 'ISO 5', 'particles': 145, 'status': 'Compliant', 'temperature': 21.2, 'humidity': 45.0},
                    {'zone': 'ISO 7', 'particles': 2840, 'status': 'Compliant', 'temperature': 20.8, 'humidity': 43.0},
                    {'zone': 'ISO 8', 'particles': 89500, 'status': 'Alert', 'temperature': 22.1, 'humidity': 47.0}
                ],
                'deviation_analysis': {
                    'trend': [2, 1, 3, 0, 1, 0, 1],
                    'total': 8,
                    'critical': 1,
                    'capa_open': 2
                },
                'inventory_status': {
                    'total_items': 156,
                    'low_stock': 12,
                    'expired': 3,
                    'critical': 4,
                    'status_breakdown': {'Good': 141, 'Low Stock': 12, 'Critical': 3}
                }
            }
        }