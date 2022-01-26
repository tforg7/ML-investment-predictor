## Project Overview 

---

## Introduction
### Our Task 

We are a new new Business group at a PA Asset Management firm tasked with leading the firms integration of Digital Assets with traditional investment porfolios. The firm is interested in exploring how two digital assets, Bitcoin & Eethereum, into its traditional investment stragegy for Conservative, Moderate, & Agressive pofilios. Our task is to recommend which & how much Digital Asset should be paied with each traditional porfolio risk profile. Susecuently, based on Market Data in the state recommend Markets to which these porfolios can be targeted too. 

For this Analysis we will need to answer: 
1. Analyze the results of the last 5 years for a traditonal Conservative, Moderate, & Agressive Porfolio for a baseline. 
2. Analyse the risk profile of Bitcoin & Eethereum: How do Ethereum and Bitcoin compare with the broader market, as represented by S&P500 Index?
3. Recomend how much of each Digital Assets should be combined with each Traditonal profilio & anlayze the outcome 
4. Anlayze Pennsylvania Census Data to recommend markets for each Porfolio 

---

## Data Sources 
Data for this presentaion was found in three parts: 
1. We research the make up of Traditional Pofolios & incorprated assets that fit the risk profolio of each profilio. 
* Conservative includes: BIV, BSV, VB, VV, VXUS
* Moderate & Agressive include: BND, VB, VV, VWO, VXUS

(Data Soruce API)

2. Bitcoin & Eethereum choosen for thier breath of data & Name recongnition to novice digital investors 

(Data Soruce from Google Finance for the last 5 years & saved as a CSV)
3. S&P data from Google Finance 

4. PA Market Data: Household Income Data Sourced from Kaggle pull from Census API
---

## Data Analysis

### Part 1. Analysis of the risk profiles of Bitcoin & Eethereum. 
Location: Crypto_Analysis.ipynb
1. Import  Libraries & Depencencies 
2. Read and Process Bitcoin, Eethereum, & SPY Data. Steps include: Setting the path, sorting the index, organizing close prices by date, preparing multi level index for monte Carlo Anlaysis
3. Calculate & Plot Daily Returns for each (Line Chats)
![ETH DR](ETHDailyReturns.jpeg)
![BTC DR](BTCDailyReturns.jpeg)
![SPY DR](SPYDailyReturns.jpeg)
4. Prepare a Pandas Dataframes for Concatenation of Daily Returns 
5. Blend Bitcoin & Eethereum with S&P, then prepare a Box Plot of Daily Returns
![Box Plot](BoxPlotDailyReturnDigital.jpeg)
6. Calculate and Plot Rolling 1y Volatility Plots using standard deviation function
![STD Plot](1yrRollingSTD.jpeg)
7. Calculate Cumulative Returns & Plot 
![total return](Cumulativereturns.jpeg)
8. Calculate Rolling Three Month Betas & Plot 
![3m rolling ETH SPY](3mRollingBetaETH&SPY.jpeg)
![3m rolling BTC&SPY](3mRollingBetaBTC&SPY.jpeg)
![3m rolling Agressive](3MRollingBetaAgressiveSPYETH&SPYBeta.jpeg)
![3m Rolling Agressive](3MRollingBetaModerate&SPY.jpeg)
9. Using a Monte Carlo Anlaysis perform a one year projection of Ethereum. Plot Daily Returns of the simulation. Then simulate behavior of a $10,000 Inbvestment & Plot Returns
![1yr DR ETH](FinalSimulatedDailyReturnsBehaviprofETHovernextyear.jpeg)
![10k 1 yr returns ETH](SimulatedReturnsETH10k.jpeg)
10. Using a Monte Carlo Anlaysis perform a one year projection of S&P. Plot Daily Returns of the simulation. Then simulate behavior of a $10,000 Inbvestment & Plot Returns.
![1yrDRSPY](SimulatedDailyReturnsofSPYnext year.jpeg)
![10k 1 yr returns SPY](10kInvestSPYSimulation.jpeg)
11. Using a Monte Carlo Anlaysis perform a one year projection of Bitcoin. Plot Daily Returns of the simulation. Then simulate behavior of a $10,000 Inbvestment & Plot Returns.
![1yr DR BTC](SimulatedDRBTCoverthenextyear.jpeg)
![10k 1 yr returns BTC](10KSimulatedReturnsBTC.jpeg)
12. Analysis of outcomes 
![Adnan results](Adnantable.jpeg)

#### Part 2. Anlysis of Traditional Pofolios 
Location: project_1_all_portfolios.ipynb
1. Import  Libraries & Depencencies, Load .env variables, Set alpaca key and Secret key
2. Set weigths of a Conservative Moderate & Aggresive porfolios 
3. Run a Monte Carolo Simulation of a Conservative Porfolio: Plot Returns & Note Summary Statistics
![CON MCline](ConservMCLine.jpeg)
![Con MCDis](ConservMCdis.jpeg)
![Con MCSS](SummarystatsCONSMC.jpeg)
4. Run a Monte Carolo Simulation of a Moderate Porfolio: Plot Returns & Note Summary Statistics
![MOD MCline](MODMCLine.jpeg)
![MOD MCDis](MODMCDIS.jpeg)
![MOD MCSS](MODMCSS.jpeg)
5. Run a Monte Carolo Simulation of a Agressive Porfolio: Plot Returns & Note Summary Statistics
![Agr MCline](AgressMCLine.jpeg)
![ARG MCDis](AggresMCDis.jpeg)
![ARG MCSS](AgressMCSS.jpeg)
6. Calculate & Plot Returns of each simulation
![Con por](Aggressiveporfolioreturns.jpeg)
![MOD poris](Moderateporfolioreturns.jpeg)
![ARG por](Aggressiveporfolioreturns.jpeg)
7. Calulate Porfolio Betas & Sharpe Ratios 
8. Summarize Benchmark Statistics 
## Part 3. Anlysis of Combined Porfolios
Location: project_1_all_portfolios.ipynb
1. From the end of the analysis in PArt 1 Combine data gathered for digital assets in part 2 with the porfolios in part 1. 
* Set Porfolio weights 
* Clean data to show close prices 
2. Define assets and weights for conservative portfolio with 2% digital assets
3. Define assets and weights for moderate portfolio with 5% digital assets
4. Define assets and weights for aggressive portfolio with 10% digital assets
5. Find cumulative returns for all 3 portfolios with digital assets
![COM AG](Combinedagress.jpeg)
![COM MOD](Combinedmod.jpeg)
![COMB CON](Combinedcons.jpeg)
6. Run a Monte Carolo Simulation of a Conservative Porfolio: Plot Returns & Note Summary Statistics
![Crypto con MCline](CryptocombinedMCline.jpeg)
![Crypto con CDis](CryptocombinedMCdis.jpeg)
![Crypto con MCSS](CryptocombinedMClSS.jpeg)

7. Run a Monte Carolo Simulation of a Moderate Porfolio: Plot Returns & Note Summary Statistics
![MOD CZR MCline](MODCRMCLINE.jpeg)
![MOD CR MCDis](MODCRMCDIS.jpeg)
![MOD CR MCSS](MODCRMCDD.jpeg)
8. Run a Monte Carolo Simulation of a Agressive Porfolio: Plot Returns & Note Summary Statistics

![Agr CR MCline](CRAGRESSMCLINE.jpeg)
![ARG MCDis](CRAGRESSMCDIS.jpeg)
![ARG MCSS](CRAGRESSMCSS.jpeg)
9. Find Beta and Sharpe Ratios for all portfolios
![Mike Table](Miketable.jpeg)

## Part 4. Anlysis of PA Household Income Data
Location: PA Household Income by City.ipynb
1. Import  Libraries & Depencencies, Load .env variables, Set alpaca key and Secret key
2. Loadin in Census Data sourced from Kaggle 
3. Creat a Mapbox Plot to visulatize the Market Data. 
![Map Box PA](MapboxPA.jpeg)

--- 

## Conclusions & Results 
Based on our analysis our recomendations for integrating digital assets into traditional investment profilios are as follows: Conservative 2% digital, Moderate 5% digital, Agressive 10% digital. 

Test Results 
Results: Average yearly returns
* Conservative +6.9%
* Moderate +13.3%
* Agressive +22.1%

Results: Monte Carlo Ratio
* Conservative +3.0%
* Moderate +7.5%
* Agressive +12.2%

Results: Beta change
* Conservative +.26
* Moderate +1.0
* Agressive +1.7

Results: Sharpe Ratio change
* Conservative +.36
* Moderate +.55
* Agressive +.87 (1)

Note: unexpected result that the sharpe ratio of an agressive digital belended portfolio produced a higher Sharpe Ratio)

After combining the digital assets with traditional investment porfolios we found that digital assets raised the average yearly returns as expected. The results of a 1 year forward looking Monte Carlo simulation confimed these results. Based on the volitility metrics, the digital assets increased risk and volitlity substantially for conservative and moderate investors. Therefore, the firm should target an agressive investor, with a high risk tolerance, with a higher beta traditonal portfolio combined with a higher allocation (10%) digital assets. Based on the Greater Philadelphia Market household income data our firm will be tageting indiviuals in the citys of Philadelphia, West Chester, Ardmore, and Wayne as they have the largest average hosuehold incomes. Assumption being that households with higher incomes have higher savings. Therefore these households will have a higher risk tolorence.

---

## Implications 
In a real life scienero not all investors are the same. Thus they will not always follow the exact risk profilie identified in this analysis. An example of this could be a traditonal agressive investor that wants to get into the digital asset market. When presented with the outcomes of our analysis they decide that the increased risk is not worth the increased return. But, we could pitch to this individual that he/she can achive similar returns for less risk & be in the digital asset market by choosing the conservative profolio integrated with digital assets. Which has compareable returns but lowers risk while postioning them in the digital market. 




