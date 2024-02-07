from time import perf_counter

from scraper.scrapy_test import deploy_crawler
import pandas as pd


if __name__ == "__main__":
    print(
        "\n"
        + "\n================================================================="
        + "\n||                        ORACLE-ESTATE                        ||"
        + "\n================================================================="
        + "\n"
    )

    t = perf_counter()

    deploy_crawler()

    #to rename columns if needed
    
    df = pd.read_csv('output.csv')
    df2 = df.rename(columns = {'id':"Property ID"}, inplace = False)
    df2.to_csv("output.csv")



    
    print("\nFinal time taken to scrape specs on all the properties:", perf_counter() - t)
        
        