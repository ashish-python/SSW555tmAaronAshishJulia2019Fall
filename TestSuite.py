import unittest
import TimeUtils
from Project import GedcomParse
import datetime

class TestSuite(unittest.TestCase):

    #User Story - 38
    #List upcoming birthdays
    #The file has birthdays that are today, in exactly 30 days, within the 30 day range, after 30 days, and birthday's that have passed
    def test_us38(self):
        parser = GedcomParse()
        parser.parseFile("US_38.txt")
        today_str = "18 SEP 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_38(today)
        self.assertEqual(parser.us38_list,[[6, 'US38-I01', 'James /Cook/', '24 SEP'], [0, 'US38-I02', 'Jessica /Cook/', '18 SEP'], [30, 'US38-I05', 'Rita /Fuller/', '18 OCT']])
    
    #User Story - 42
    #Reject illegitimate dates
    def test_us42(self):
        parser = GedcomParse()
        self.assertEqual(TimeUtils.legitimate_date("30 FEB 2009"), False)
        self.assertEqual(TimeUtils.legitimate_date("0 JAN 2009"), False)
        self.assertEqual(TimeUtils.legitimate_date("DEC 2009"), False)
        self.assertEqual(TimeUtils.legitimate_date("MAR"), False)
        self.assertEqual(TimeUtils.legitimate_date("2019"), False)
        self.assertNotEqual(TimeUtils.legitimate_date("29 FEB 2020"), False) #Leap year
    
    #User Story - 01 
    #Finds any date that is after the current date
    def test_us01(self):
        parser = GedcomParse()
        parser.parseFile("US_01.txt")
        today_str = "29 SEP 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_01(today)
        self.assertEqual(parser.us01_list, [['Birth', datetime.date(2099, 7, 13), 'US01-I01', 'Han /Solo/'], ['Birth', datetime.date(3140, 10, 21), 'US01-I02', 'Leia /Skywalker/'], ['Death', datetime.date(3490, 12, 27), 'US01-I02', 'Leia /Skywalker/'], ['Death', datetime.date(2022, 10, 21), 'US01-I04', 'Padme /Amidala/'], ['Divorce', datetime.date(2990, 4, 8), 'US01-F01'], ['Marriage', datetime.date(2980, 5, 9), 'US01-F01']])

    #User Story - 22
    #Finds any repeated IDs 
    def test_us22(self):
        parser = GedcomParse()
        parser.parseFile("US_22.txt")
        self.assertEqual(parser.us22_list, [['INDI', 'US22-I01'], ['INDI', 'US22-I02'], ['FAM', 'US22-F01']])

    #User Story - 04
    #Marriage date before divorce date
    def test_us04(self):
        parser = GedcomParse()
        parser.parseFile("US_04.txt")
        parser.us_04()
        self.assertEqual(parser.us04_list,[['08 Jul 2010', '08 Jul 2020', 'F06']])

    #User Story - 05
    #Marriage date before death date
    def test_us05(self):
        parser = GedcomParse()
        parser.parseFile("US_05.txt")
        parser.us_05()
        self.assertEqual(parser.us05_list,[['F05', 'US05-I10', 'Randi /Gold/', '10 Oct 1985', '10 Jun 1984']])
    
    #User Story - 36
    #List recent deaths
    #The test file has deaths that are today, exactly 30 days ago, within the last 30 days, before the last 30 days, and date in the future
    def test_us36(self):
        parser = GedcomParse()
        parser.parseFile("US_36.txt")
        today_str = "02 OCT 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_36(today)
        self.assertEqual(parser.us36_list,[[-7, 'US36-I01', 'James /Cook/', '25 Sep 2019'], [0, 'US36-I02', 'Jessica /Cook/', '02 Oct 2019'], [-30, 'US36-I05', 'Rita /Fuller/', '02 Sep 2019']])

    #User Story - 35
    #List recent births
    #The test file has births that are today, exactly 30 days ago, within the last 30 days, before the last 30 days, and a date in the future
    def test_us35(self):
        parser = GedcomParse()
        parser.parseFile("US_35.txt")
        today_str = "02 OCT 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_35(today)
        self.assertEqual(parser.us35_list, [[-7, 'US35-I01', 'James /Cook/', '25 Sep 2019'], [0, 'US35-I02', 'Jessica /Cook/', '02 Oct 2019'], [-30, 'US35-I05', 'Rita /Fuller/', '02 Sep 2019']])
    
    #User Story - 08
    #Birth before marriage and/or 9 months after divorce
    def test_us08(self):
        parser = GedcomParse()
        parser.parseFile("US_08.txt")
        parser.us_08()
        self.assertEqual(parser.us08_list,[['Divorce', 'Benjamin /Solo/', 'US08-I5', '19 Nov 1991', '08 Apr 1990'], ['Marriage', 'Han /Solo/', 'US08-I1', '13 Jul 1942', '04 Aug 1950']])
    
    #User Story - 16
    #All male members of a family should have the same last name
    def test_us16(self):
        parser = GedcomParse()
        parser.parseFile("US_16.txt")
        parser.us_16()
        self.assertEqual(parser.us16_list,[['Benjamin /Ford/', 'Han /Solo/', 'US16-F1'], ['Jacen /Hamill/', 'Luke /Skywalker/', 'US16-F4']])

    #User Story - 06
    #Death before divorce
    def test_us06(self):
        parser = GedcomParse()
        parser.parseFile("US_06.txt")
        parser.us_06()
        self.assertEqual(parser.us06_list,[['F06', 'US06-I12', 'Jill /Maisel/', '08 Jul 1990', '05 Nov 1980']])

    #User Story - 07
    #Less than 150 years old
    def test_us07(self):
        parser = GedcomParse()
        parser.parseFile("US_07.txt")
        today_str = "09 OCT 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y")
        parser.us_07(today)
        self.assertEqual(parser.us07_list, [['death_after_150', 'US07-I99', 'William /Burr/', '05 Jun 1850', '19 Dec 2001'], ['alive_over_150', 'US07-I01', 'Julia /Cahn/', '16 Sep 1800', '09 Oct 2019']])
    
    #User Story - 30
    #Living married people
    def test_us30(self):
        parser = GedcomParse()
        parser.parseFile("US_30.txt")
        parser.us_30()
        self.assertEqual(parser.us30_list,[['Husband', 'US30-F01', 'US30-I01', 'James /Cook/'], ['Wife', 'US30-F01', 'US30-I02', 'Jessica /Cook/']])


    #User Story - 31
    #Under 30 and never been married
    def test_us31(self):
        parser = GedcomParse()
        parser.parseFile("US_31.txt")
        today_str = "14 OCT 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_31(today)
        self.assertEqual(parser.us31_list,[['US31-I03', 'Samantha /Hayes/', '09 May 1977', 42], ['US31-I05', 'Robbie /Williams/', '13 Oct 1989', 30]])

    #User Story - 23
    #Unique names
    def test_us23(self):
        parser = GedcomParse()
        parser.parseFile("US_23.txt")
        parser.us_23()
        self.assertEqual(parser.us23_list, [
            ['Birthday', 'Luke /Skywalker/', 'US23-I6', '21 Oct 1956'], 
            ['Birthday', 'Mara /Jade/', 'US23-I7', '21 Oct 1956'], 
            ['Name', 'Luke /Skywalker/', 'US23-I8']])

    #User Story - 24
    #Unique spouses and marriage dates
    def test_us24(self):
        parser = GedcomParse() 
        parser.parseFile("US_24.txt")
        parser.us_24()
        self.assertEqual(parser.us24_list, [['WIFE', '04 Aug 1940', 'Padme /Amidala/', 'US24-F3', 'US24-F2']])

    #User Story - 09
    #Birth before death of parents
    def test_us09(self):
        parser = GedcomParse()
        parser.parseFile("US_09.txt")
        today_str = "25 OCT 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_09()
        self.assertEqual(parser.us09_list,[['US09-I11', 'US09-I09', '06 Feb 3000', '10 Jun 1900'], ['US09-I11', 'US09-I10', '06 Feb 3000', '10 Jun 1900']])

    #User Story - 11
    # No bigamy
    def test_us11(self):
        parser = GedcomParse()
        parser.parseFile("US_11.txt")
        parser.us_11()
        self.assertEqual(parser.us11_list, [['marriage before divorce', 'US11-I01', 'James /Cook/', 'US11-F01', 'US11-F02', '06 Feb 2007', '19 Sep 2010', '10 Dec 2015'], ['same date marriage', 'US11-I01', 'James /Cook/', 'US11-F01', 'US11-F99', '06 Feb 2007'], ['marriage before death', 'US11-I40', 'Sanjay /Shaw/', 'US11-F41', 'US11-F42', '06 Feb 2000', '19 Sep 2005', '06 Jun 2007']])

    #User Story-29: List all deaceased individuals
    def test_us29(self):
        parser = GedcomParse()
        parser.parseFile("US_29.txt")
        today_str = "31 OCT 2019"
        today = datetime.datetime.strptime(today_str, "%d %b %Y").date()
        parser.us_29(today)
        self.assertEqual(parser.us29_list, [['US29-I01', 'James /Cook/', '30 Jun 2019']])

    #User Story-34: List all couples who were married when the older spouse was more than twice as old as the younger spouse --#
    def test_us34(self):
        parser = GedcomParse()
        parser.parseFile("US_34.txt")
        parser.us_34()
        self.assertEqual(parser.us34_list, [['US34-F01', '25 Sep 1989', 'US34-I02', 'Jessica /Cook/', '25 Sep 1969', 20, 'US34-I01', 'James /Cook/', '25 Sep 1949', 40]])

    #User Story 15 - Less than 15 siblings in a family
    def test_us15(self):
        parser = GedcomParse()
        parser.parseFile("US_15.txt")
        parser.us_15()
        self.assertEqual(parser.us15_list,[['US15-F1', 19, {'US15-I18', 'US15-I13', 'US15-I05', 'US15-I07', 'US15-I14', 'US15-I04', 'US15-I09', 'US15-I11', 'US15-I20', 'US15-I06', 'US15-I08', 'US15-I12', 'US15-I15', 'US15-I01', 'US15-I21', 'US15-I17', 'US15-I19', 'US15-I16', 'US15-I10'}]])
    
    #User Story 21: Correct roles for sex. Husband should be male. Wife should be female.
    def test_us21(self):
        parser = GedcomParse()
        parser.parseFile("US_21.txt")
        parser.us_21()
        self.assertEqual(parser.us21_list, [['F1', 'I02', 'Adam /Cahn/', 'Husband', 'F'], ['F1', 'I03', 'Alisa /Cahn/', 'Wife', 'M']])
    
    #User Story 18
    # Siblings cant marry each other
    def test_us18(self):
        parser = GedcomParse()
        parser.parseFile("US_18.txt")
        parser.us_18()
        self.assertEqual(parser.us18_list, [['US18-I9', 'US18-I8']])
    
    #User Story 17
    # Parents cant marry their children
    def test_us17(self):
        parser = GedcomParse()
        parser.parseFile("US_17.txt")
        parser.us_17()
        self.assertEqual(parser.us17_list, [['DAD', 'US17-I5', 'Benjamin /Solo/', 'US17-I2', 'Leia /Skywalker/']])
if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)