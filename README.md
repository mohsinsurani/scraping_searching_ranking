# scraping_searching_ranking

Scraping Search Ranking
Sausage Shop is a Web application designed to provide the information on the research professors available on the website. Built using Dart as the primary language and FlutterUI Material design as the frontend framework, the app offers a user-friendly interface for users to stay informed about the operational status of research articles of the professor.

Key Features:

Comprehensive Research Status: Get instant information on whether the article is closed or open, and the research publication done by the professor.
Technology Stack:

Language: Dart (Front end), Python (backend) for scrapping from other websites
Frontend Framework: FlutterUI Material design
How It Works: The app leverages Dart to handle the application logic using BLoC and Flutter widgets for creating an intuitive and responsive user interface. Users can easily navigate through the app to access detailed information about articles on professor detail screen.

It ensures a seamless user experience, providing critical information at a glance and helping commuters make informed decisions about their sausages.

Running and tested Version:

Flutter 3.16.5 • channel stable
Dart 3.2.3 • DevTools 2.28.4
XCode 14.2
iOS 16.2 deployment target
iPhone Landscape and Portrait support
MacOS Monterey 12.7.2
How to build the code?

Checkout the main branch
run flutter run -- ios on VSCode

Run the groups in vscode to check the total price calculations.
Any Assumptions?

This app currently only targets iPhone models and not any other devices and do not support Android currently.
My old Macbook doesn't contain USB-C Port so was unable to test this app on iPhone device and my iPhone currently runs on iOS 17.
Offline information was saved in shared preference such as sausageList selected by the users.
Meal time calculation was assumed breakfast ( 5 to 11), Lunch (11 to 16), Snack (16 to 19), Dinner (19 to 22) and Closed (22 to 5). This calculation was done using system time zones.
Sausage availability is based upon the provided json's available from and to dates.
Any Relevant Inputs?

It was fun and exciting to work on this project and get to learn many things.
Tried to use maximum of enums, BLoC, MaterialUI, Optional, error-handling and rules to support this reactive approach.
Created a few folders as so to decrease the burden of all logics and it can be splitted in various forms.
