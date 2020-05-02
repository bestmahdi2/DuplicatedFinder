# DuplicatedFinder
This is a python script to find duplicated files in a directory 

این یک برنامه پایتون برای پیدا کردن فایل های تکراری در یک دایرکتوری است
***

**/Main directory/**

DuplicatedFinder.py : main script

Deleter.py : script to keep original file and remove all duplicated files.

## How to use DuplicatedFinder:
Open **CMD** or **PowerShell** on Windows and type:

    python dupFinder.py folder1 folder2 folder3

Open **Terminal** on Linux and type:
    
    python3 dupFinder.py folder1 folder2 folder3

You can replace folder with path of directory you want to find duplicated files.

.میتوانید مسیر دایرکتوری مورد نظر خود را جای فولدر بنویسید

Then files will go to  "duplicated_files" in script directory .

.بعد از اجرا کردن برنامه فایل ها به صورت خودکار در مسیر بالا کپی میشوند


## How to use Deleter:
Copy the script in duplicated_files directory , then it keeps the original file and removes the rest files. if it doesn't find the original file , it keeps one and removes the rest.

آن را در دایرکتوری بالا کپی کنید ، بعد فایل اصلی را بین فایل ها پیدا کرده و بقیه را حذف میکند ، اگر فایل اصلی را پیدا نکند یکی را نگه داشته و بقیه را پاک میکند.

Then بعد :

Open **CMD** or **PowerShell** on Windows and type:
      
    python Deleter.py [-r] [-p]
   -r : Move to RecycleBin
   , -p : Permanently delete , 
and you can't use both -r and -s together


Open **Terminal** on Linux and type:

    python3  Deleter.py [-r] [-p]
   -r : Move to RecycleBin
   , -p : Permanently delete , 
and you can't use both -r and -s together


## Notice:
There is a Right_path.txt in every directory which tells you where the files where in the first place , so don't worry about missing files locations.

 یک فایل متنی در هر دایرکتوری وجود دارد که در آن مسیر درست هر کدام از فایل ها در آن آورده شده ، پس نگران گم شدن مسیر فایل ها نباشید

***
Based on python 3 , so may not be used in windows Xp , 98 and ...

بر اساس پایتون 3 ، غیرقابل استفاده در ویندوز ایکس پی ، 98 و غیره 

You may want to change file type ("destinationDir") in DuplicatedFinder script to search for your favorite Directory.

.شاید دوست داشته باشید دایرکتوری فایل ها (متغییر بالا) را جایگزین دایرکتوری مورد نظرتان کنید 
