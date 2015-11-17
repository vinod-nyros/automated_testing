'''
from mindprod.com java app:

   /*
    From http://www.icverify.com/
    Vendor        Prefix len      checkdigit
    MASTERCARD    51-55  16       mod 10
    VISA          4      13, 16   mod 10
    AMEX          34,37  15       mod 10
    Diners Club/
    Carte Blanche
                 300-305 14
                 36      14
                 38      14       mod 10
    Discover     6011    16       mod 10
    enRoute      2014    15
                 2149    15       any
    JCB          3       16       mod 10
    JCB          2131    15
                 1800    15       mod 10  */

Also:
Date: 5 Oct 2000 07:22:37 -0000
From: python-finance@egroups.com

Python impl of Luhn's formula, with bug fixed by JJW
'''

from string import digits

def numbersOnly (s):  # remove non-numbers
  result = ''

  for c in s:
    if c in digits:
      result = result + c

  return result
  

def vendor (n):
  s = str (n)
  l = len (s)
  unknown = '(unknown card type)' 

  if not l:
    return unknown

  one = int (s [0])
  two = int (s [:2])
  three = int (s [:3])
  four = int (s [:4])

  if two >= 51 and two <= 55:
    return 'MasterCard'
  elif one ==4:
    return 'Visa'
  elif l == 15 and (two == 34 or two == 37):
    return 'Amex'
  elif l == 14 and (three >= 300 and three <= 305 or two == 36 or two == 38):
    return "Diner's"
  elif four == 6011:
    return 'Discover'
  elif four == 2014 or four == 2149:
    return 'EnRoute'
  elif (l == 16 and one == 3) or (l == 15 and (four == 2131 or four == 1800)):
    return 'JCB'
  else:
    return unknown
  

maptable = (0,2,4,6,8,1,3,5,7,9)

def validate (s):
  s = numbersOnly (s)
  l = len (s) + 1
  cd = 0

  if l == 1 or l > 17: return 0  # blank is invalid!
  
  for i in range (-2, -l, -2):
    cd = cd + maptable [int (s[i])]

  for i in range (-1, -l, -2):
    cd = cd + int (s[i])

  return cd % 10 == 0


if __name__ == "__main__":    
  print validate       ('4190 0877 0645 ')
  print validate       ('3852 271017 ')
  print validate       ('6011 0005 8021 ')
  print validate       ('5588-0002-0045-')
  print validate       ('5588-0002-0345-')
  
