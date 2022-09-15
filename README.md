# 🌄 ACC-student-outdoors-club

![image](https://user-images.githubusercontent.com/102194829/189515197-30678274-6c67-4887-894e-e08e35b53add.png)

---

## 👋  Introduction

This productivity app was designed to help speed up the workflow of its ACC users. The manual task of collecting student submissions, 
formatting and preparing said data for the database is a lengthy error-prone process. Most importantly, the addresses
need to be accurate and in a strict format which will initiate downstream problems if not inputted correctly.

This app aims to automate this process by leveraging Canada Post's API. It reduced manual errors and made sure that submitted addresses were legitimate.

---

## 🤷‍♂️  Who is this for? 

ACC employees looking to off-load repetitve tasks and speed up their work-flow

---

## 💪  Packages/Dependencies/Sources used 
urllib | numpy | pandas | xml.dom.minidom | IPython.display | copy



---

## 😵 Class / Method Summary

**class correctACCsubmission()**:
- is a tool that helps automate the processes involved with ACC Group Submissions. 
- It takes information from an xcel sheet (a member form submission) and formats the data in a way that allows for an IMIS submission. 
- the Perfect_Template.xlsx is a heading only excel file that serves as an empty base template, that once filled, will be submitted to the IMIS database. The xlsx file is imported, and a panda series is created.
- the ACC_MailOut_Template.xlsx is a form filled out by an ACC member and submitted back to an ACC agent. 
       
**class AddressComplete()**:
- is a collection of functions that handle the input, and return, of an address (a string) and its submission to the Canada Post API. 
- In addition, functions dealing with the selection and input behaviours help navigate the Canada Post suggestions that exist 


 ---

## 🍪  Things to add

Obtain your API-KEY from Canada-Post (https://www.canadapost-postescanada.ca/ac/) and then navigate to wrapper() located in 'ACC_Main.py' to enter your credentials/API-Key. 

Obtain a completed xlsx file from the student group and input said filepath in wrapper(), located in 'ACC_Main.py'
 
 ---

## 🔨  Improvements on the Application

This application uses a terminal style interface and leverages IPython.display tools to help functionality and style. 
A web based app with authentication would be more intuitive for users. The terminal style requires knowledge of python which could be a boundary for others. 

The app's data could benefit from dynamic state changes, thus chosing a framework like React would be helpful.

---

 
 Have fun testing and improving it! 😎
