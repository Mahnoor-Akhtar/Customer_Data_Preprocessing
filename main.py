"""
CUSTOMERS DATASET PREPROCESSING SYSTEM
Dataset Fields: Index, Customer Id, First Name, Last Name, Company, City, Country, 
                Phone 1, Phone 2, Email, Subscription Date, Website
"""

import pandas as pd

class CustomersPreprocessor:
    """Main class for customers data preprocessing operations"""
    
    def __init__(self):
        self.dataset = None
        self.cleaned_data = None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("CUSTOMERS DATA PREPROCESSING SYSTEM")
        print("="*70)
        print("\n1. Load Customers Dataset")
        print("2. Explore Dataset")
        print("3. Analyze Data Quality")
        print("4. Clean Dataset")
        print("5. Export Cleaned Data")
        print("6. Exit")
        print("="*70)
    
    def load_dataset(self):
        """Load the customers dataset from CSV file"""
        print("\n[1] LOADING CUSTOMERS DATASET")
        print("-"*50)
        
        try:
            self.dataset = pd.read_csv("customers-100000.csv")
            print("✅ Dataset loaded successfully!")
            print(f"   📊 Records: {len(self.dataset):,}")
            print(f"   📈 Columns: {len(self.dataset.columns)}")
            
            # Display column information
            print("\n   📋 Dataset Structure:")
            print("   " + "-"*45)
            for i, col in enumerate(self.dataset.columns, 1):
                print(f"   {i:2}. {col:20} ({self.dataset[col].dtype})")
            
            return True
        except FileNotFoundError:
            print("❌ Error: 'customers-100000.csv' not found!")
            print("   Please ensure the file is in the same directory.")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def explore_dataset(self):
        """Explore and describe the dataset"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[2] DATASET EXPLORATION")
        print("-"*50)
        
        # Basic information
        print("\n📊 BASIC INFORMATION:")
        print(f"   • Total Customers: {len(self.dataset):,}")
        print(f"   • Total Columns: {len(self.dataset.columns)}")
        print(f"   • Dataset Shape: {self.dataset.shape}")
        
        # Data types
        print("\n📝 DATA TYPES:")
        dtype_counts = self.dataset.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"   • {dtype}: {count} columns")
        
        # First few records
        print("\n👥 SAMPLE CUSTOMERS (First 3 records):")
        print(self.dataset.head(3).to_string(index=False))
        
        # Country distribution
        if 'Country' in self.dataset.columns:
            print("\n🌍 COUNTRY DISTRIBUTION:")
            country_counts = self.dataset['Country'].value_counts().head(5)
            for country, count in country_counts.items():
                percentage = (count / len(self.dataset)) * 100
                print(f"   • {country}: {count} customers ({percentage:.1f}%)")
        
        # City distribution
        if 'City' in self.dataset.columns:
            print("\n🏙️  TOP CITIES:")
            city_counts = self.dataset['City'].value_counts().head(5)
            for city, count in city_counts.items():
                if pd.notna(city):
                    percentage = (count / len(self.dataset)) * 100
                    print(f"   • {city}: {count} customers ({percentage:.1f}%)")
        
        # Company statistics
        if 'Company' in self.dataset.columns:
            print("\n🏢 COMPANY ANALYSIS:")
            companies_with_data = self.dataset['Company'].notna().sum()
            percentage_with_company = (companies_with_data / len(self.dataset)) * 100
            print(f"   • Customers with company: {companies_with_data:,} ({percentage_with_company:.1f}%)")
            
            unique_companies = self.dataset['Company'].nunique()
            print(f"   • Unique companies: {unique_companies:,}")
        
        # Subscription date analysis
        if 'Subscription Date' in self.dataset.columns:
            print("\n📅 SUBSCRIPTION DATE ANALYSIS:")
            try:
                self.dataset['Subscription Date'] = pd.to_datetime(self.dataset['Subscription Date'], errors='coerce')
                oldest = self.dataset['Subscription Date'].min()
                newest = self.dataset['Subscription Date'].max()
                print(f"   • Oldest subscription: {oldest.date()}")
                print(f"   • Newest subscription: {newest.date()}")
                
                # Yearly subscription count
                yearly_counts = self.dataset['Subscription Date'].dt.year.value_counts().sort_index()
                print(f"   • Subscriptions by year:")
                for year, count in yearly_counts.items():
                    print(f"      {year}: {count:,} customers")
            except:
                print("   • Could not analyze subscription dates")
        
        # Email domain analysis
        if 'Email' in self.dataset.columns:
            print("\n📧 EMAIL DOMAIN ANALYSIS:")
            # Extract domains from emails
            def extract_domain(email):
                if pd.isna(email) or '@' not in str(email):
                    return 'Unknown'
                return str(email).split('@')[-1].lower()
            
            domains = self.dataset['Email'].apply(extract_domain)
            top_domains = domains.value_counts().head(5)
            for domain, count in top_domains.items():
                percentage = (count / len(self.dataset)) * 100
                print(f"   • {domain}: {count} ({percentage:.1f}%)")
    
    def analyze_quality(self):
        """Analyze data quality issues"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[3] DATA QUALITY ANALYSIS")
        print("-"*50)
        
        issues = []
        
        # 1. Check for missing values
        print("\n🔍 MISSING VALUES ANALYSIS:")
        missing_data = self.dataset.isnull().sum()
        total_missing = missing_data.sum()
        
        if total_missing > 0:
            issues.append(f"Missing Values ({total_missing} total)")
            print(f"   ❌ Total missing values: {total_missing}")
            for col, count in missing_data.items():
                if count > 0:
                    percentage = (count / len(self.dataset)) * 100
                    print(f"      • {col}: {count} ({percentage:.1f}%)")
        else:
            print("   ✅ No missing values found")
        
        # 2. Check for duplicates
        print("\n🔍 DUPLICATE CUSTOMERS ANALYSIS:")
        duplicates = self.dataset.duplicated().sum()
        
        if duplicates > 0:
            issues.append(f"Duplicate Customers ({duplicates} found)")
            print(f"   ❌ Duplicate customers: {duplicates}")
            
            # Show duplicate examples
            duplicate_rows = self.dataset[self.dataset.duplicated()]
            print(f"\n   📄 Example of duplicate customers:")
            print(duplicate_rows.head(2).to_string(index=False))
        else:
            print("   ✅ No duplicate customers found")
        
        # 3. Check Customer Id uniqueness
        if 'Customer Id' in self.dataset.columns:
            print("\n🔍 CUSTOMER ID UNIQUENESS:")
            unique_ids = self.dataset['Customer Id'].nunique()
            total_ids = len(self.dataset)
            if unique_ids < total_ids:
                issues.append(f"Non-unique Customer IDs ({total_ids - unique_ids} duplicates)")
                print(f"   ❌ Customer ID duplicates: {total_ids - unique_ids}")
                print(f"   • Unique IDs: {unique_ids:,}")
                print(f"   • Total records: {total_ids:,}")
            else:
                print("   ✅ All Customer IDs are unique")
        
        # 4. Email validation
        if 'Email' in self.dataset.columns:
            print("\n🔍 EMAIL VALIDATION:")
            invalid_emails = self.dataset['Email'].apply(
                lambda x: pd.notna(x) and '@' not in str(x)
            ).sum()
            if invalid_emails > 0:
                issues.append(f"Invalid Emails ({invalid_emails} found)")
                print(f"   ❌ Invalid emails (missing @): {invalid_emails}")
            else:
                print("   ✅ All emails have valid format")
        
        # 5. Phone validation
        for phone_col in ['Phone 1', 'Phone 2']:
            if phone_col in self.dataset.columns:
                print(f"\n🔍 {phone_col.upper()} VALIDATION:")
                phone_missing = self.dataset[phone_col].isnull().sum()
                if phone_missing > 0:
                    percentage = (phone_missing / len(self.dataset)) * 100
                    print(f"   ⚠️  Missing {phone_col.lower()}: {phone_missing} ({percentage:.1f}%)")
                
                # Check phone format (simple validation)
                def is_valid_phone(phone):
                    if pd.isna(phone):
                        return True  # Missing is okay
                    phone_str = str(phone)
                    # Count digits
                    digit_count = sum(c.isdigit() for c in phone_str)
                    return digit_count >= 7  # Minimum 7 digits
                
                invalid_phones = self.dataset[phone_col].apply(
                    lambda x: not is_valid_phone(x)
                ).sum()
                if invalid_phones > 0:
                    issues.append(f"Invalid {phone_col} ({invalid_phones} found)")
                    print(f"   ❌ Invalid {phone_col.lower()}: {invalid_phones}")
        
        # 6. Subscription date validation
        if 'Subscription Date' in self.dataset.columns:
            print("\n🔍 SUBSCRIPTION DATE VALIDATION:")
            try:
                dates = pd.to_datetime(self.dataset['Subscription Date'], errors='coerce')
                invalid_dates = dates.isnull().sum()
                if invalid_dates > 0:
                    issues.append(f"Invalid Subscription Dates ({invalid_dates} found)")
                    print(f"   ❌ Invalid subscription dates: {invalid_dates}")
                else:
                    print("   ✅ All subscription dates are valid")
            except:
                print("   ⚠️  Could not validate subscription dates")
        
        # Summary
        print("\n" + "="*50)
        print("QUALITY SUMMARY:")
        if issues:
            print("❌ Issues detected:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ Excellent data quality - No issues detected!")
        print("="*50)
    
    def clean_dataset(self):
        """Clean the dataset"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[4] DATA CLEANING PROCESS")
        print("-"*50)
        
        # Create a copy for cleaning
        self.cleaned_data = self.dataset.copy()
        
        print("Starting cleaning process...\n")
        
        # Step 1: Remove duplicates
        initial_count = len(self.cleaned_data)
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        final_count = len(self.cleaned_data)
        duplicates_removed = initial_count - final_count
        
        if duplicates_removed > 0:
            print(f"✅ STEP 1: Removed {duplicates_removed} duplicate customers")
        else:
            print("✅ STEP 1: No duplicates to remove")
        
        # Step 2: Handle missing values
        print("\n✅ STEP 2: Handling missing values")
        
        # Fill missing first names
        if 'First Name' in self.cleaned_data.columns:
            firstname_missing = self.cleaned_data['First Name'].isnull().sum()
            if firstname_missing > 0:
                self.cleaned_data['First Name'] = self.cleaned_data['First Name'].fillna('Unknown')
                print(f"   • Filled {firstname_missing} missing first names")
        
        # Fill missing last names
        if 'Last Name' in self.cleaned_data.columns:
            lastname_missing = self.cleaned_data['Last Name'].isnull().sum()
            if lastname_missing > 0:
                self.cleaned_data['Last Name'] = self.cleaned_data['Last Name'].fillna('Unknown')
                print(f"   • Filled {lastname_missing} missing last names")
        
        # Fill missing companies
        if 'Company' in self.cleaned_data.columns:
            company_missing = self.cleaned_data['Company'].isnull().sum()
            if company_missing > 0:
                self.cleaned_data['Company'] = self.cleaned_data['Company'].fillna('Individual')
                print(f"   • Filled {company_missing} missing companies")
        
        # Fill missing cities
        if 'City' in self.cleaned_data.columns:
            city_missing = self.cleaned_data['City'].isnull().sum()
            if city_missing > 0:
                # Use mode (most common city) for filling
                mode_city = self.cleaned_data['City'].mode()[0] if not self.cleaned_data['City'].mode().empty else 'Unknown'
                self.cleaned_data['City'] = self.cleaned_data['City'].fillna(mode_city)
                print(f"   • Filled {city_missing} missing cities with '{mode_city}'")
        
        # Fill missing countries
        if 'Country' in self.cleaned_data.columns:
            country_missing = self.cleaned_data['Country'].isnull().sum()
            if country_missing > 0:
                # Use mode (most common country) for filling
                mode_country = self.cleaned_data['Country'].mode()[0] if not self.cleaned_data['Country'].mode().empty else 'Unknown'
                self.cleaned_data['Country'] = self.cleaned_data['Country'].fillna(mode_country)
                print(f"   • Filled {country_missing} missing countries with '{mode_country}'")
        
        # Fill missing emails
        if 'Email' in self.cleaned_data.columns:
            email_missing = self.cleaned_data['Email'].isnull().sum()
            if email_missing > 0:
                # Create email from first and last name
                def generate_email(row):
                    if pd.notna(row['Email']):
                        return row['Email']
                    first = str(row['First Name']).lower().replace(' ', '')
                    last = str(row['Last Name']).lower().replace(' ', '')
                    return f"{first}.{last}@no-email.com"
                
                self.cleaned_data['Email'] = self.cleaned_data.apply(generate_email, axis=1)
                print(f"   • Generated {email_missing} missing emails")
        
        # Fill missing websites
        if 'Website' in self.cleaned_data.columns:
            website_missing = self.cleaned_data['Website'].isnull().sum()
            if website_missing > 0:
                self.cleaned_data['Website'] = self.cleaned_data['Website'].fillna('no-website.com')
                print(f"   • Filled {website_missing} missing websites")
        
        # Step 3: Data standardization
        print("\n✅ STEP 3: Standardizing data formats")
        
        # Standardize names (title case)
        if 'First Name' in self.cleaned_data.columns:
            self.cleaned_data['First Name'] = self.cleaned_data['First Name'].str.title()
            print("   • Standardized first names (Title Case)")
        
        if 'Last Name' in self.cleaned_data.columns:
            self.cleaned_data['Last Name'] = self.cleaned_data['Last Name'].str.title()
            print("   • Standardized last names (Title Case)")
        
        # Standardize company names
        if 'Company' in self.cleaned_data.columns:
            self.cleaned_data['Company'] = self.cleaned_data['Company'].apply(
                lambda x: str(x).title() if pd.notna(x) and x != 'Individual' else x
            )
            print("   • Standardized company names")
        
        # Standardize phone format
        for phone_col in ['Phone 1', 'Phone 2']:
            if phone_col in self.cleaned_data.columns:
                def format_phone(phone):
                    if pd.isna(phone):
                        return ''
                    # Remove all non-digit characters
                    digits = ''.join(c for c in str(phone) if c.isdigit())
                    if len(digits) >= 10:
                        return f"{digits[:3]}-{digits[3:6]}-{digits[6:10]}"
                    elif len(digits) >= 7:
                        return f"{digits[:3]}-{digits[3:7]}"
                    else:
                        return digits
                
                self.cleaned_data[phone_col] = self.cleaned_data[phone_col].apply(format_phone)
                print(f"   • Standardized {phone_col} format")
        
        # Standardize email (lowercase)
        if 'Email' in self.cleaned_data.columns:
            self.cleaned_data['Email'] = self.cleaned_data['Email'].str.lower()
            print("   • Standardized emails (lowercase)")
        
        # Standardize website format
        if 'Website' in self.cleaned_data.columns:
            def format_website(url):
                if pd.isna(url) or url == 'no-website.com':
                    return url
                url = str(url).strip().lower()
                if not url.startswith('http'):
                    return f'https://{url}'
                return url
            
            self.cleaned_data['Website'] = self.cleaned_data['Website'].apply(format_website)
            print("   • Standardized website URLs")
        
        # Convert Subscription Date to datetime
        if 'Subscription Date' in self.cleaned_data.columns:
            try:
                self.cleaned_data['Subscription Date'] = pd.to_datetime(
                    self.cleaned_data['Subscription Date'], errors='coerce'
                )
                # Fill invalid dates with most recent date
                recent_date = self.cleaned_data['Subscription Date'].max()
                self.cleaned_data['Subscription Date'] = self.cleaned_data['Subscription Date'].fillna(recent_date)
                print("   • Standardized subscription dates")
            except:
                print("   • Could not standardize subscription dates")
        
        # Step 4: Create full name column
        print("\n✅ STEP 4: Creating derived columns")
        self.cleaned_data['Full Name'] = self.cleaned_data['First Name'] + ' ' + self.cleaned_data['Last Name']
        print("   • Created 'Full Name' column")
        
        # Create primary contact phone
        self.cleaned_data['Primary Phone'] = self.cleaned_data['Phone 1'].combine_first(self.cleaned_data.get('Phone 2', ''))
        print("   • Created 'Primary Phone' column")
        
        # Summary
        print("\n" + "="*50)
        print("CLEANING COMPLETE!")
        print(f"Original customers: {initial_count:,}")
        print(f"Cleaned customers: {final_count:,}")
        print(f"Customers removed: {duplicates_removed}")
        
        # Show cleaning impact
        print("\n📊 CLEANING IMPACT:")
        print(f"   • Missing values before: {self.dataset.isnull().sum().sum()}")
        print(f"   • Missing values after: {self.cleaned_data.isnull().sum().sum()}")
        print(f"   • Duplicates before: {self.dataset.duplicated().sum()}")
        print(f"   • Duplicates after: {self.cleaned_data.duplicated().sum()}")
        
        # Show new columns
        new_cols = set(self.cleaned_data.columns) - set(self.dataset.columns)
        if new_cols:
            print(f"   • New columns added: {', '.join(new_cols)}")
        
        print("="*50)
        
        # Show cleaned data sample
        print("\n👥 CLEANED CUSTOMERS SAMPLE:")
        display_cols = ['Customer Id', 'Full Name', 'Company', 'Country', 'Email', 'Subscription Date']
        display_cols = [col for col in display_cols if col in self.cleaned_data.columns]
        print(self.cleaned_data[display_cols].head(3).to_string(index=False))
    
    def export_data(self):
        """Export cleaned data to CSV"""
        if self.cleaned_data is None:
            print("❌ Please clean dataset first (Option 4)")
            return
        
        print("\n[5] EXPORT CLEANED DATA")
        print("-"*50)
        
        filename = "cleaned_customers_dataset.csv"
        
        try:
            self.cleaned_data.to_csv(filename, index=False)
            
            print(f"✅ Data exported successfully!")
            print(f"\n📁 FILE DETAILS:")
            print(f"   • Filename: {filename}")
            print(f"   • Customers: {len(self.cleaned_data):,}")
            print(f"   • Columns: {len(self.cleaned_data.columns)}")
            print(f"   • File size: ~{len(self.cleaned_data) * len(self.cleaned_data.columns):,} data points")
            
            # Top countries in exported data
            if 'Country' in self.cleaned_data.columns:
                print(f"\n🌍 TOP COUNTRIES:")
                country_summary = self.cleaned_data['Country'].value_counts().head(5)
                for country, count in country_summary.items():
                    percentage = (count / len(self.cleaned_data)) * 100
                    print(f"   • {country}: {count:,} customers ({percentage:.1f}%)")
            
            # Subscription year summary
            if 'Subscription Date' in self.cleaned_data.columns:
                try:
                    self.cleaned_data['Subscription Year'] = pd.to_datetime(
                        self.cleaned_data['Subscription Date']
                    ).dt.year
                    print(f"\n📅 SUBSCRIPTIONS BY YEAR:")
                    year_summary = self.cleaned_data['Subscription Year'].value_counts().sort_index()
                    for year, count in year_summary.items():
                        percentage = (count / len(self.cleaned_data)) * 100
                        print(f"   • {year}: {count:,} customers ({percentage:.1f}%)")
                except:
                    pass
            
            # Email domain summary
            if 'Email' in self.cleaned_data.columns:
                print(f"\n📧 TOP EMAIL DOMAINS:")
                def get_domain(email):
                    if '@' in str(email):
                        return str(email).split('@')[-1]
                    return 'unknown'
                
                domains = self.cleaned_data['Email'].apply(get_domain)
                domain_summary = domains.value_counts().head(5)
                for domain, count in domain_summary.items():
                    percentage = (count / len(self.cleaned_data)) * 100
                    print(f"   • {domain}: {count:,} customers ({percentage:.1f}%)")
            
            print(f"\n📍 File saved as: {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def run(self):
        """Main program loop"""
        print("\n" + "="*70)
        print("CUSTOMERS DATA PREPROCESSING SYSTEM")
        print("="*70)
        print("\nDataset Fields (12 columns):")
        print("1. Index            2. Customer Id       3. First Name")
        print("4. Last Name        5. Company           6. City")
        print("7. Country          8. Phone 1           9. Phone 2")
        print("10. Email          11. Subscription Date 12. Website")
        print("="*70)
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.load_dataset()
            elif choice == '2':
                self.explore_dataset()
            elif choice == '3':
                self.analyze_quality()
            elif choice == '4':
                self.clean_dataset()
            elif choice == '5':
                self.export_data()
            elif choice == '6':
                print("\n" + "="*70)
                print("THANK YOU FOR USING CUSTOMERS DATA PREPROCESSING SYSTEM")
                print("="*70)
                break
            else:
                print("❌ Invalid choice! Please enter 1-6")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    processor = CustomersPreprocessor()
    processor.run()

if __name__ == "__main__":
    main()