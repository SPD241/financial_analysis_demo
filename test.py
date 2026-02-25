import data_extract_node as den

extractor = den.DataExtractor()
extractor.get_data(symbol='EURUSD=X', start_date='2023-01-01', end_date='2023-06-01')
extractor.plot_data()
extractor.get_data_as_csv()