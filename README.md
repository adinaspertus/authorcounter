# authorcounter
Adina Spertus & Ofer Dotan,
December 2020

In this project we created a classifier using supervised machine learning that predicts the number of authors (single vs. multiple) of an academic article and the decade it was written (1990s-2020s). The two predicition functions for the decade and author count are written using the Sklearn package. To exhibit the results, we developed a TKinter App in which an abstract/a short text can be inserted to receive the model prediciton as an output. 

To run the program: 
1. please separately download the Cornell University arXiv dataset from: https://www.kaggle.com/Cornell-University/arxiv
2. final_project: this file contains the model;
3. functions: this file contains functions we defined and are used in both final_project and authorcounter_app
4. authorcounter_app: this file contains the Tkinter app to demonstrate how the model works.

Note: Originally the program was developed with the intention of considering absolute number of authors (not just single vs. multiple) and year (not just decade). These options are still available in the code, just commented out. 
