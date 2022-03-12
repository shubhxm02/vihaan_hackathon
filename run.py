from Name_and_pricefound import execution_of_orders



def get_stock_main(username, password, screener_link,instance):
    instance.open_screener(screener_link)
    instance.runscan()

    # Till here we have clicked run scan button and have list of all stocks scanned by screener
    list_stock_urls_chart_link, list_of_stock_names, j = instance.list_of_stocks()
    print(j)
    print(list_stock_urls_chart_link)
    print(list_of_stock_names)
    trend_list = instance.supertrend_finder(list_stock_urls_chart_link, j)
    print(trend_list)
    return trend_list

