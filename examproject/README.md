# Examproject
**Group name: MCB** 

**Group members: MFQ992, NVF696, RXW556**

**Handed in 25th of May 2019** 

### Introduction 
In this portfolio the reader will find a collection of the group's projects: Dataproject, modelproject and suggested answers to the exam questions.

The file *Dataproject.ipynb* is a Jupyter Notebook file containing our data project of Standard & Poor's (S&P) 500 **stock price movements**.

The file *Modelproject.ipynb* is a Jupter Notebook file containing our model project of a **static and two-period Real Business Cycle (RBC) model**.

The file *exam_2019.ipynb* is a Jupyter Notebook file containing our suggested answers to the questions provided in the original file of the same name. It provides data description and visualization of a utility maximization through **human capital accumulation, the aggregated demand and aggregated supply (AS-AD) model** as well as a **model of an exchange economy**. 

Below the reader will find a more detailed description of each project.

### Dataproject

The purpose of this project is to gather stock data from the S&P500 using Yahoo's native API and the package *BeautifulSoup* to webscrabe a list of the company tickers, and from there feed it into CSV-files and lastly consolidate it into a single CSV-file. From there we create a chart comparing one of the companies from S&P500 to the S&P500 benchmark. We chose 2016/01/04 arbitrarily as our start date with an end date at 2019/05/20.

The project includes interactive widgets allowing the user to chose his/her desired tickers for comparison and provides visualization of both the **adjusted close price, indexed values, relative percentage changes** and a **correlation table**. 

###  Modelproject

The purpose of this project is to showcase the static and two-period RBC model, based on the model presented in Macroeconomics III. 
We model an **intertemporal household optimization problem**, where we define a utility function in which a household or individual seeks to maximize his or her utility in a two-period scenario given an endowment of leisure. The model is based on discrete time. For reference one might look at Romer, D., "Advanced Macroeconomics", *McGraw Hill, 4th Edition*, 2012.

Specifically, we model the trade-off between leisure and consumption and derive the optimal consumption smoothing path based on given parameter values of risk aversion, preference for leisure and the intertemporal elasticity of substitution. In our project we also consider the effects of changes in the parameters and present figures for each parameter. We consider examples of a single- and two-period model and derive the optimal bundle of consumption and leisure.

### Exam questions
We provide our suggested answers to the three problems defined in the *exam_2019.ipynb* file. 

Problem 1 consists of solving an utility optimization problem using a model of labour as a function of human capital in a two-period scenario. We solve the model and find the relevant break points and visualize our results. We also provide interactive floatsliders where the user can see the effects of changing the wage rate, unemployment benefits and the aversion to work.

Problem 2 consists of solving an AS-AD model and find the optimal inflation rate as well as output rate. We solve the model under certain assumptions about shocks, parameter values, and starting point in one period that then changes to the next. We then optimize the model to find parameter values that will give a specific variance for inflation and output, as well as corralation between the two. 


Problem 3 description. 
