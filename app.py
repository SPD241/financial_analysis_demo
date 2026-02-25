import streamlit as st
import pandas as pd
import numpy as np
import data_extract_node as den
from constants import FOREX_PAIRS, PERIOD, TITLE_MESSAGE, HEADER_MESSAGE, PAIR_SELECT_BOX_MESSAGE, PERIOD_SELECT_BOX_MESSAGE, COL2_MESSAGE, URL_IMAGE, ANALYSIS_TOOLS
from gemini_client import prompt
import gemini_client

class Streamlit_App:

    def __init__(self) -> None:
        '''
        HERE WE DEFINED ALL SELF VARIABLES THAT COULD BE NECESSARY IN ALL CODE
        '''
        st.title(TITLE_MESSAGE)
        self.col1, self.col2, self.col3 = st.columns(3)
        with self.col1:
            st.image(URL_IMAGE, width=300)
        with self.col2:
            st.write(COL2_MESSAGE)
        with self.col3:
            st.sidebar.title("Options")

            self.options = st.sidebar.selectbox("Select Option", ["Data Extraction", "Models AI", "Analysis Tools", "About us"])

        self.extractor = den.DataExtractor()
        self.data = None


        if "data" not in st.session_state:
            st.session_state["data"] = None
        
        if "analysis_outputs" not in st.session_state:
            st.session_state["analysis_outputs"] = {}
        
        

    def interface (self) -> None:
        '''
        THIS CODE CREATES THE STREAMLIT INTERFACE CONNECTING WITH SOME FUNCTIONS FROM data_extract_node.py
        '''
        if self.options == "Data Extraction":
            st.header(HEADER_MESSAGE)

            self.pair = st.selectbox(PAIR_SELECT_BOX_MESSAGE, FOREX_PAIRS)
            self.interval = st.selectbox(PERIOD_SELECT_BOX_MESSAGE, PERIOD)

            self.start_day = st.date_input("Select start date")
            self.end_day = st.date_input("Select end date")

            if st.button("Extract Data"):
                self.data = self.extractor.get_data(symbol=self.pair, start_date=self.start_day, end_date=self.end_day, interval=self.interval)
                st.line_chart(self.data[['Close','Open','High','Low']])
                st.session_state["data"] = self.data
        
        elif self.options == "Models AI":

            
            

            data = st.session_state["data"]
            st.header("AI Models Section")
            if data is None:
                print("Please extract data first")
                return
            else:
                outputs = st.session_state.get("analysis_outputs", {})

                rsi_obj = outputs.get("RSI")
                macd_df = outputs.get("MACD")

                rsi_last = rsi_obj["RSI"].dropna().iloc[-1].item()
                macd_last = macd_df["MACD"].dropna().iloc[-1].item()
                signal_last = macd_df["Signal"].dropna().iloc[-1].item()

                develop_prompt = prompt(rsi_last = rsi_last, macd_last= macd_last, signal_last = signal_last)
                gemini = gemini_client.Generative_Model.chat(prompt=develop_prompt)
                st.success("Model creation and data preprocessing complete.")

                st.write("AI assistant suggestion: \n" , gemini)

        
        elif self.options == "Analysis Tools":

            '''
            HERE WE CALLED analysis_tools.py FOR SOME TECHNIQUES (THE MOST POPULAR) FOR TRADING TENDENCES.
            '''
            data = st.session_state["data"]
            st.header("Analysis Tools Section")
            
            self.analysis_tools = st.selectbox("Select Analysis Tool", ANALYSIS_TOOLS)

            if data is None: 
                print("Please extract data first")
                return
            else:
                st.success("Model creation and data preprocessing complete.")
                data = pd.DataFrame(data)
                from analysis_tools import AnalysisTools
                tools = AnalysisTools()

                

                if self.analysis_tools == "RSI":
                    rsi = tools.Relative_Strength_Index(data=data)
                    st.session_state["analysis_outputs"]["RSI"] = rsi

                    st.line_chart(rsi[["RS", "RSI"]])

                
                elif self.analysis_tools == "MACD":
                    macd = tools.macd(data=data)
                    st.session_state["analysis_outputs"]["MACD"] = macd

                    st.line_chart(macd[["MACD","Signal"]])
                    st.bar_chart(macd["Histogram"])
                
                elif self.analysis_tools == "Bollinger Bands":
                    bb = tools.bollinger_bands(data = data)
                    plot_df = pd.concat([data["Close"], bb], axis=1)
                    st.session_state["analysis_outputs"]["BB"] = bb
                    st.line_chart(plot_df[["Close","MB","UB","LB"]])

                elif self.analysis_tools == "Moving Averages":
                    ma = tools.moving_average(data=data)
                    st.line_chart(ma)

                elif self.analysis_tools == "Candlestick Patterns":
                    cp = tools.bollinger_bands(data=data)
                    st.dataframe(cp[cp.any(axis=1)].tail(50))

                elif self.analysis_tools == "Ichimoku Cloud Analysis":
                    ic = tools.ichimoku_cloud(data=data)
                    st.session_state["analysis_outputs"]["ICHIMOKU"] = ic
                    plot_df = pd.concat([data["Close"], ic], axis=1)
                    st.line_chart(plot_df)
                

if __name__ == "__main__":
    app = Streamlit_App()
    app.interface()