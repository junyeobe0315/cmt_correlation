# Python code for Genome-wide association studies for CMT1A patients-specific methylation patterns

# Intro

Charcot-Marie-Tooth disease type 1A (CMT1A) is caused by 17p12 region duplication, but clinical hetrogeneity ranges from mild to severe.

This study was performed to determine whether epigenetic factors affected to severity.

---

# Used Libraries
- python : 3.10
* numpy 
- pandas : most important used
* matplotlib
- scipy
* tqdm

---
# Used Dataset

The subject were investigated in 11 unaffected individuals (42.2 0xB1; 3.4 years old) and 22 CMT1A patients (46.4 0xB1; 3.5 years old) in male.

Using the SureSelectXT Methy-Seq Library Kit, the methylation levels of a total of 66,279,954 CpG sites were measured.

<img width="593" alt="Screenshot 2022-12-15 at 4 28 27 PM" src="https://user-images.githubusercontent.com/83803247/207806119-6cd1df47-ba02-4387-b802-442464cbc388.png">
    
    fig 1. example of dataset

# Python code

* CMT1A_vs_Control_t_test.py

    <img width="1124" alt="Screenshot 2022-12-14 at 3 32 10 PM" src="https://user-images.githubusercontent.com/83803247/207805893-826f2498-6c43-4ac6-a1ae-87e479b67b31.png">
    
        fig 2. pesudo code
 
    <img width="331" alt="Screenshot 2022-12-15 at 5 09 54 PM" src="https://user-images.githubusercontent.com/83803247/207807522-9055b672-7229-4c92-a1f8-02e2633c068e.png">
    
        fig 3. Levene's test

    <img width="762" alt="Screenshot 2022-12-15 at 5 17 37 PM" src="https://user-images.githubusercontent.com/83803247/207808037-796aacc2-e274-4d8c-931f-93069bf71cc7.png">

        fig 4. Student's t-test

    In CMT1A_vs_Control_t_test.py we used Levene's test to check normality.  

    If the p-value of Levene's test is over 0.05 (In case of Equal variance) we used Student's test of equal variance to check the t value of position.

    If the p-value of Levene's test is under 0.05 (In case of non-Equal variance) we used Student's test of non-equal variance to check the t value of position.


    The plot below is the result of Student's t-test.


    <img width="267" alt="Screenshot 2022-12-16 at 1 31 54 PM" src="https://user-images.githubusercontent.com/83803247/208022734-7b687bb0-4c5d-429a-8c13-33da93b9001e.png">

        fig 5. Manhattan Plot of the result


- correlation.py

    This code to analyze the correlation between methylation level and cmtns.

    Assumed cmtns and methylation level to be continuous and proceeded with the following analysis.

    <img width="1283" alt="Screenshot 2022-12-20 at 4 51 55 PM" src="https://user-images.githubusercontent.com/83803247/208612747-faf2a0b6-64cb-4dbd-a658-76bda5f73f5f.png">

        fig 6. Pseudo-code of correlation.py

    <img width="381" alt="Screenshot 2022-12-20 at 4 57 52 PM" src="https://user-images.githubusercontent.com/83803247/208613845-81984901-4a45-4ef8-afd7-35e29d52a99a.png">
        
        fig 7. Pearson Correlation Coefficient
    
    <img width="275" alt="Screenshot 2022-12-20 at 5 02 01 PM" src="https://user-images.githubusercontent.com/83803247/208614606-74d3c7ba-cf4c-4b8e-89d4-39a45d15c820.png">
        
        fig 8. Spearman's correlation coefficient



* vis_cor.py / vis_qqplot.py

    These two codes were used to plot the correlation visualization and qqplot, respectively.

    ![example_1](https://user-images.githubusercontent.com/83803247/208644487-fe52e5c1-c734-41cb-8104-ed422d52e432.png)
    
    ![example_2](https://user-images.githubusercontent.com/83803247/208644698-8e1e7bb0-d43d-4ae2-9221-896f426fcdbd.png)

        fig 8. example images from result of vis_cor.py
    
    