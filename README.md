<img src="https://user-images.githubusercontent.com/44107852/214130084-354b95f2-abbb-43e2-bb5c-783662243ce2.jpg" align="right"
     alt="Size Limit logo by Anton Lovchikov" width="90" height="90">
# FUNDAMENTAL STOCK VALUATION DASHBOARD

This program was built to analyze fundamental financial data information of companies listed in the Brazilian stock market.

<p align="center">
  <a href="#how-it-works">How it works</a> •
  <a href="#installation-and-configuration">Installation and configuration</a> •
  <a href="#how-to-use">How to use</a> •
  <a href="#notes-and-considerations">Notes and considerations</a> •
</p>

![stock_dash](https://user-images.githubusercontent.com/44107852/214133601-c483f940-4e92-4a68-a7d7-a214b76c478c.gif)

## How it Works  

Using the python language, we can obtain fundamental financial data information from brazilian companies from [FUNDAMENTUS](https://fundamentus.com.br/) through the Fundamentus API available at https://pypi.org/project/fundamentus/.
With Dash and Plotly libraries we use the data set to build a dashboard to compare companies by each sector, indicator and the corresponding average.
In addiction, the general data table can be downloaded to an excel file and the sector and subsector table can be updated periodically or on demand.  

## Installation and configuration 

```
# Clone this repository
git clone https://github.com/GiovannaBezerra/fundamental_stock_valuation_dashboard.git

# Install development dependencies
pip install pandas
pip instal fundamentus
pip install flask==2.1.0
pip install dash
pip install dash-bootstrap-components
pip install plotly
```

## How to use

To start the interactive program, simply run **fundamental_stock_valuation_dashboard.py**.  

![img_readme1](https://user-images.githubusercontent.com/44107852/214311118-100c4974-1f27-4b65-9687-9cea8aaa5dec.jpg)

Fundamental Stock Valuation Dashboard is now running and can be accessed by pointing a web browser at http://127.0.0.1:8050/.  

![img_readme3](https://user-images.githubusercontent.com/44107852/214311240-aef2cbaf-17d9-422d-9e0a-55a7993978d5.jpg)

The dashboard can be accessed now.  

![img_readme2](https://user-images.githubusercontent.com/44107852/214311416-68664cc2-dacc-4217-8814-fce4b1d74d09.jpg)


## Notes and considerations

During this development, I've learned how to use Dash and Plotly libraries, which was very challenging for me, in particular because of layout building and callbacks construction.
