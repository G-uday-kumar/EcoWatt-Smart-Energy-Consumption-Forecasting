import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_generator import generate_energy_data
from model import prepare_data, train_model, predict_future, load_model, save_model
import os

def user_dashboard():
    """User dashboard with navigation bar and enhanced UI"""
    st.set_page_config(page_title="EcoWatt: Smart Energy Consumption Forecasting", page_icon="⚡")

    if not st.session_state.get('logged_in') or st.session_state.get('user_type') != 'user':
        st.error("Access denied. User login required.")
        return

    # Custom CSS for user dashboard theme
    st.markdown("""
    <style>
    .user-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .user-info {
        float: right;
        color: white;
        font-size: 14px;
        margin-top: 10px;
    }
    .nav-button {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 10px 20px;
        margin: 5px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
    .nav-button.active {
        background-color: rgba(255, 255, 255, 0.4);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with user info
    st.markdown(f"""
    <div class="user-dashboard">
        <h1 style="margin: 0; display: inline-block;">⚡ EcoWatt: Smart Energy Consumption Forecasting</h1>
        <div class="user-info">
            <strong>User:</strong> {st.session_state.user['full_name']}<br>
            <strong>Email:</strong> {st.session_state.user['email']}<br>
            <strong>Role:</strong> {st.session_state.user['role'].title()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation bar
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1:
        if st.button("📤 Upload Data", key="nav_upload", use_container_width=True):
            st.session_state.nav_page = "upload"
    with col2:
        if st.button("📊 Analyze Data", key="nav_analyze", use_container_width=True):
            st.session_state.nav_page = "analyze"
    with col3:
        if st.button("🔮 Forecast", key="nav_forecast", use_container_width=True):
            st.session_state.nav_page = "forecast"
    with col4:
        if st.button("📈 Results", key="nav_results", use_container_width=True):
            st.session_state.nav_page = "results"
    with col5:
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Set default page
    if 'nav_page' not in st.session_state:
        st.session_state.nav_page = "upload"

    # Page content based on navigation
    page = st.session_state.nav_page

    # Initialize data and model on first load
    if 'data' not in st.session_state:
        # Try to load existing data
        if os.path.exists('energy_data.csv'):
            try:
                data = pd.read_csv('energy_data.csv')
                data['date'] = pd.to_datetime(data['date'])
                st.session_state.data = data
            except:
                pass

    if 'model' not in st.session_state:
        # Try to load existing model
        model = load_model()
        if model:
            st.session_state.model = model

    # Page content based on navigation
    if page == "upload":
        st.header("📤 Upload Energy Data")
        st.markdown("Upload your historical energy consumption data or generate synthetic data for analysis.")

        # Show current data status
        if 'data' in st.session_state:
            data = st.session_state.data
            st.success(f"✅ Data loaded: {len(data)} records from {data['date'].min().date()} to {data['date'].max().date()}")
            st.info("💡 You can proceed to Analyze Data tab or generate new data below.")

        # Option to generate or upload data
        data_option = st.selectbox("Data Source", ["Generate Synthetic Data", "Upload CSV"], key="data_source")

        if data_option == "Generate Synthetic Data":
            st.subheader("Generate Synthetic Data")
            periods = st.slider("Number of days", 365, 365*5, 730, key="periods")
            if st.button("Generate Data", key="generate_btn"):
                with st.spinner("Generating synthetic energy consumption data..."):
                    data = generate_energy_data(periods=periods)
                    data.to_csv('energy_data.csv', index=False)
                    st.session_state.data = data
                    st.success("✅ Data generated successfully!")
                    st.info("📊 Data saved as 'energy_data.csv' - you can now analyze it in the next tab!")
                    st.balloons()
        else:
            st.subheader("Upload Your Data")
            uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="upload_file")
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                # Check if required columns exist
                if 'date' not in data.columns or 'consumption_kwh' not in data.columns:
                    st.error("❌ CSV must contain 'date' and 'consumption_kwh' columns. Please check your file format.")
                    st.info("📋 Required columns: date, consumption_kwh")
                    st.info("🕒 Optional: time (HH:MM:SS format)")
                    st.info("📝 Example: date=2023-01-01, time=14:30:00, consumption_kwh=150.5")
                else:
                    try:
                        # Handle date and optional time columns
                        if 'time' in data.columns:
                            # Combine date and time if time column exists
                            data['date'] = pd.to_datetime(data['date'] + ' ' + data['time'], format='%Y-%m-%d %H:%M:%S')
                        else:
                            # Use date only
                            data['date'] = pd.to_datetime(data['date'])

                        # Sort by date to ensure chronological order
                        data = data.sort_values('date').reset_index(drop=True)

                        st.session_state.data = data
                        st.success("✅ Data uploaded successfully!")
                        if 'time' in data.columns:
                            st.info("📅 Date and time columns combined successfully.")
                        else:
                            st.info("📅 Date column processed successfully.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error processing date/time columns: {str(e)}")
                        st.info("📅 Date format: YYYY-MM-DD (e.g., 2023-01-01)")
                        st.info("🕒 Time format (optional): HH:MM:SS (e.g., 14:30:00)")

    elif page == "analyze":
        st.header("📊 Analyze Energy Data")
        st.markdown("Explore and analyze your energy consumption patterns.")

        if 'data' in st.session_state:
            data = st.session_state.data

            # Data overview with enhanced metrics
            st.subheader("📈 Data Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Records", len(data))
            with col2:
                st.metric("📅 Date Range", f"{data['date'].min().date()} to {data['date'].max().date()}")
            with col3:
                st.metric("⚡ Avg Consumption", f"{data['consumption_kwh'].mean():.1f} kWh")
            with col4:
                st.metric("🔋 Total Consumption", f"{data['consumption_kwh'].sum():.0f} kWh")

            # Time series plot with enhanced visualization
            st.subheader("📈 Consumption Over Time")
            fig, ax = plt.subplots(figsize=(14, 7))
            ax.plot(data['date'], data['consumption_kwh'], linewidth=2, color='#1f77b4', alpha=0.8)
            ax.fill_between(data['date'], data['consumption_kwh'], alpha=0.3, color='#1f77b4')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Consumption (kWh)', fontsize=12)
            ax.set_title('Historical Energy Consumption Trends', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

            # Statistical analysis with insights
            st.subheader("📊 Statistical Analysis & Insights")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📋 Basic Statistics**")
                stats_df = data['consumption_kwh'].describe()
                st.dataframe(stats_df.apply(lambda x: f"{x:.2f}"), use_container_width=True)

                # Key insights
                st.markdown("**💡 Key Insights**")
                max_consumption = data['consumption_kwh'].max()
                min_consumption = data['consumption_kwh'].min()
                std_dev = data['consumption_kwh'].std()
                st.info(f"🔺 Peak consumption: {max_consumption:.1f} kWh")
                st.info(f"🔻 Lowest consumption: {min_consumption:.1f} kWh")
                st.info(f"📊 Variability (Std Dev): {std_dev:.1f} kWh")

            with col2:
                st.markdown("**📅 Monthly Trends**")
                data_copy = data.copy()
                data_copy['month'] = data_copy['date'].dt.month
                data_copy['month_name'] = data_copy['date'].dt.strftime('%B')
                monthly_avg = data_copy.groupby(['month', 'month_name'])['consumption_kwh'].mean().reset_index()
                monthly_avg = monthly_avg.sort_values('month')

                fig, ax = plt.subplots(figsize=(10, 5))
                bars = ax.bar(monthly_avg['month_name'], monthly_avg['consumption_kwh'],
                             color='#ff7f0e', alpha=0.7, edgecolor='black', linewidth=1)
                ax.set_xlabel('Month', fontsize=12)
                ax.set_ylabel('Average Consumption (kWh)', fontsize=12)
                ax.set_title('Monthly Average Consumption', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='y')
                ax.tick_params(axis='x', rotation=45)

                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=10)

                st.pyplot(fig)

            # Peak consumption analysis
            st.subheader("🔍 Peak Consumption Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📈 Daily Patterns**")
                data_copy = data.copy()
                data_copy['hour'] = data_copy['date'].dt.hour
                hourly_avg = data_copy.groupby('hour')['consumption_kwh'].mean()

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linewidth=2, color='#2ca02c')
                ax.set_xlabel('Hour of Day')
                ax.set_ylabel('Average Consumption (kWh)')
                ax.set_title('Average Consumption by Hour')
                ax.grid(True, alpha=0.3)
                ax.set_xticks(range(0, 24, 2))
                st.pyplot(fig)

            with col2:
                st.markdown("**📊 Consumption Distribution**")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(data['consumption_kwh'], bins=30, alpha=0.7, color='#d62728', edgecolor='black')
                ax.set_xlabel('Consumption (kWh)')
                ax.set_ylabel('Frequency')
                ax.set_title('Consumption Distribution')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

            # Model training section with enhanced feedback
            st.subheader("🤖 AI Model Training")
            st.markdown("Train a machine learning model to forecast future energy consumption.")

            if 'model' in st.session_state:
                st.success("✅ Forecasting model is already trained and ready!")
                st.info("💡 You can proceed to generate forecasts in the next tab.")
            else:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("""
                    **What the model does:**
                    - Learns patterns from your historical data
                    - Uses time series forecasting techniques
                    - Predicts future consumption based on past trends
                    """)
                with col2:
                    if st.button("🚀 Train Forecasting Model", key="train_model", use_container_width=True):
                        with st.spinner("🤖 Training AI model... This may take a moment..."):
                            try:
                                X, y = prepare_data(data)
                                if len(X) < 7:
                                    st.error("❌ Need at least 7 days of data to train the model.")
                                else:
                                    model = train_model(X, y)
                                    save_model(model)
                                    st.session_state.model = model
                                    st.success("✅ AI Model trained successfully!")
                                    st.info("🎯 The model is now ready for forecasting future consumption!")
                                    st.balloons()
                            except Exception as e:
                                st.error(f"❌ Error training model: {str(e)}")
                                st.info("💡 Try with more data points or check data quality.")
        else:
            st.warning("⚠️ No data available. Please upload or generate data first in the Upload Data tab.")
            st.info("💡 Tip: Start with generating synthetic data to see how the analysis works!")

    elif page == "forecast":
        st.header("🔮 Generate Forecast")
        st.markdown("Generate AI-powered predictions for future energy consumption.")

        if 'data' in st.session_state and 'model' in st.session_state:
            data = st.session_state.data

            # Current status
            st.success("✅ Data and AI model are ready for forecasting!")

            # Forecast parameters with enhanced UI
            st.subheader("🎛️ Forecast Parameters")
            col1, col2, col3 = st.columns(3)
            with col1:
                days_ahead = st.slider("📅 Days to forecast", 1, 90, 30, key="forecast_days")
            with col2:
                confidence_level = st.selectbox("🎯 Confidence Level", ["80%", "90%", "95%"], index=1, key="confidence")
            with col3:
                forecast_type = st.selectbox("📊 Forecast Type", ["Standard", "Conservative", "Optimistic"], index=0, key="forecast_type")

            # Forecast explanation
            st.info(f"🤖 The AI will predict energy consumption for the next {days_ahead} days based on patterns learned from your historical data.")

            # Generate forecast button
            if st.button("🚀 Generate AI Forecast", key="generate_forecast", use_container_width=True, type="primary"):
                with st.spinner("🔮 AI is generating your energy consumption forecast..."):
                    try:
                        # Get last known data for prediction
                        last_known = data['consumption_kwh'].values[-7:]  # Last 7 days
                        predictions = predict_future(st.session_state.model, last_known, days_ahead)

                        # Apply forecast type adjustments
                        if forecast_type == "Conservative":
                            predictions = predictions * 0.9  # 10% reduction
                        elif forecast_type == "Optimistic":
                            predictions = predictions * 1.1  # 10% increase

                        # Create forecast dates
                        last_date = data['date'].max()
                        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days_ahead)

                        forecast_df = pd.DataFrame({
                            'date': forecast_dates,
                            'predicted_consumption': predictions
                        })

                        st.session_state.forecast = forecast_df
                        st.success(f"✅ AI Forecast generated for {days_ahead} days!")
                        st.info("📊 Check the Results tab to view your forecast and download the data!")
                        st.balloons()

                    except Exception as e:
                        st.error(f"❌ Error generating forecast: {str(e)}")
                        st.info("💡 Try training the model again or check your data.")

            # Quick preview if forecast exists
            if 'forecast' in st.session_state:
                forecast_df = st.session_state.forecast
                st.subheader("📋 Forecast Preview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📅 Forecast Period", f"{len(forecast_df)} days")
                with col2:
                    st.metric("⚡ Avg Predicted", f"{forecast_df['predicted_consumption'].mean():.1f} kWh")
                with col3:
                    st.metric("🔋 Total Predicted", f"{forecast_df['predicted_consumption'].sum():.0f} kWh")

        elif 'data' not in st.session_state:
            st.warning("⚠️ No data available. Please upload or generate data first in the Upload Data tab.")
            st.info("💡 Start by generating synthetic data to test the forecasting feature!")
        else:
            st.warning("⚠️ AI model not trained. Please train the model first in the Analyze Data tab.")
            st.info("🤖 The forecasting requires an AI model trained on your data patterns.")

    elif page == "results":
        st.header("📈 Forecast Results")
        st.markdown("View your AI-generated energy consumption predictions and insights.")

        if 'forecast' in st.session_state and 'data' in st.session_state:
            data = st.session_state.data
            forecast_df = st.session_state.forecast

            # Success message and overview
            st.success("✅ AI Forecast completed! Here are your results:")

            # Combined plot with enhanced visualization
            st.subheader("📊 Historical vs AI Forecast")
            fig, ax = plt.subplots(figsize=(16, 8))

            # Historical data
            ax.plot(data['date'], data['consumption_kwh'], label='Historical Data',
                   color='#1f77b4', linewidth=3, alpha=0.8)

            # Forecast data
            ax.plot(forecast_df['date'], forecast_df['predicted_consumption'],
                   label='AI Forecast', color='#ff7f0e', linewidth=3, linestyle='--', alpha=0.9)

            # Forecast start line
            ax.axvline(x=data['date'].max(), color='#d62728', linestyle=':', alpha=0.8, linewidth=2,
                      label='Forecast Start')

            # Fill areas
            ax.fill_between(data['date'], data['consumption_kwh'], alpha=0.2, color='#1f77b4')
            ax.fill_between(forecast_df['date'], forecast_df['predicted_consumption'],
                           alpha=0.3, color='#ff7f0e')

            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Energy Consumption (kWh)', fontsize=12, fontweight='bold')
            ax.set_title('Energy Consumption: Historical Data & AI Forecast', fontsize=16, fontweight='bold')
            ax.legend(fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)

            # Add annotations
            hist_avg = data['consumption_kwh'].mean()
            forecast_avg = forecast_df['predicted_consumption'].mean()
            ax.axhline(y=hist_avg, color='#1f77b4', linestyle='--', alpha=0.5, label=f'Historical Avg: {hist_avg:.1f}')
            ax.axhline(y=forecast_avg, color='#ff7f0e', linestyle='--', alpha=0.5, label=f'Forecast Avg: {forecast_avg:.1f}')

            st.pyplot(fig)

            # Key insights
            st.subheader("💡 AI Forecast Insights")
            col1, col2, col3, col4 = st.columns(4)

            hist_avg = data['consumption_kwh'].mean()
            forecast_avg = forecast_df['predicted_consumption'].mean()
            change_percent = ((forecast_avg - hist_avg) / hist_avg) * 100

            with col1:
                st.metric("📊 Historical Average", f"{hist_avg:.1f} kWh")
            with col2:
                st.metric("🔮 Forecast Average", f"{forecast_avg:.1f} kWh")
            with col3:
                st.metric("📈 Change", f"{change_percent:+.1f}%",
                         delta=f"{change_percent:+.1f}%" if abs(change_percent) > 1 else "Stable")
            with col4:
                st.metric("📅 Forecast Days", len(forecast_df))

            # Forecast data table with enhanced formatting
            st.subheader("📋 Detailed Forecast Data")
            display_df = forecast_df.copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            display_df['predicted_consumption'] = display_df['predicted_consumption'].round(2)

            # Add day counter
            display_df['day'] = range(1, len(display_df) + 1)
            display_df = display_df[['day', 'date', 'predicted_consumption']]

            st.dataframe(display_df.style.format({
                'predicted_consumption': '{:.2f} kWh',
                'day': '{:.0f}'
            }).set_properties(**{'text-align': 'center'}), use_container_width=True)

            # Forecast statistics with more details
            st.subheader("📈 Forecast Statistics & Analysis")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📅 Forecast Period", f"{len(forecast_df)} days")
            with col2:
                st.metric("⚡ Avg Predicted", f"{forecast_df['predicted_consumption'].mean():.1f} kWh")
            with col3:
                st.metric("🔺 Peak Predicted", f"{forecast_df['predicted_consumption'].max():.1f} kWh")
            with col4:
                st.metric("🔻 Min Predicted", f"{forecast_df['predicted_consumption'].min():.1f} kWh")

            # Additional analysis
            st.subheader("🔍 Advanced Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📊 Forecast Distribution**")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(forecast_df['predicted_consumption'], bins=20, alpha=0.7,
                       color='#ff7f0e', edgecolor='black', linewidth=1)
                ax.set_xlabel('Predicted Consumption (kWh)')
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

            with col2:
                st.markdown("**📈 Forecast Trend**")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(forecast_df['day'], forecast_df['predicted_consumption'],
                       marker='o', linewidth=2, color='#2ca02c', markersize=4)
                ax.set_xlabel('Day')
                ax.set_ylabel('Predicted Consumption (kWh)')
                ax.set_title('Forecast Trend Over Time')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

            # Download options with enhanced UI
            st.subheader("💾 Download Your Results")
            st.markdown("Export your AI forecast data for further analysis or reporting.")

            col1, col2, col3 = st.columns(3)
            with col1:
                csv_forecast = forecast_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Forecast CSV",
                    data=csv_forecast,
                    file_name=f"energy_forecast_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="download_forecast",
                    use_container_width=True
                )

            with col2:
                # Combined historical + forecast data
                combined_df = pd.concat([
                    data[['date', 'consumption_kwh']].assign(data_type='historical'),
                    forecast_df.rename(columns={'predicted_consumption': 'consumption_kwh'}).assign(data_type='forecast')
                ], ignore_index=True)
                csv_combined = combined_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Combined Data CSV",
                    data=csv_combined,
                    file_name=f"energy_data_complete_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="download_combined",
                    use_container_width=True
                )

            with col3:
                # Summary report
                summary_data = {
                    'Metric': ['Historical Period', 'Forecast Period', 'Historical Average', 'Forecast Average',
                              'Change %', 'Peak Historical', 'Peak Forecast'],
                    'Value': [
                        f"{data['date'].min().date()} to {data['date'].max().date()}",
                        f"{forecast_df['date'].min().date()} to {forecast_df['date'].max().date()}",
                        f"{hist_avg:.2f} kWh",
                        f"{forecast_avg:.2f} kWh",
                        f"{change_percent:+.2f}%",
                        f"{data['consumption_kwh'].max():.2f} kWh",
                        f"{forecast_df['predicted_consumption'].max():.2f} kWh"
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                csv_summary = summary_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Summary Report",
                    data=csv_summary,
                    file_name=f"forecast_summary_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="download_summary",
                    use_container_width=True
                )

            # Final message
            st.success("🎉 Your AI-powered energy consumption forecast is complete!")
            st.info("💡 Use this data for planning, budgeting, or optimizing your energy usage.")

        else:
            st.warning("⚠️ No forecast available. Please generate a forecast first in the Forecast tab.")
            st.info("🔮 Go to the 'Generate Forecast' tab to create AI predictions for your energy consumption.")


