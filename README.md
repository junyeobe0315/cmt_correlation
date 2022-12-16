# Python code for Genome-wide association studies for CMT1A patients-specific methylation patterns

# Intro

Charcot-Marie-Tooth disease type 1A (CMT1A) is caused by 17p12 region duplication, but clinical hetrogeneity ranges from mild to severe.

This study was performed to determine whether epigenetic factors affected to severity.

---

# Used Libraries
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

in CMT1A_vs_Control_t_test.py we used

- correlation.py



* vis_cor.py
- vis_qqplot.py

