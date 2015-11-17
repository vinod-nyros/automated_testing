import tags

states= ( \
("Alabama", "AX"), 			\
("Alaska", "AK"), 			\
("American Samoa", "AS"), 		\
("Arizona", "AZ"), 			\
("Arkansas", "AR"), 			\
("Armed Forces Africa", "AE"),          \
("Armed Forces Americas (except Canada)", "AA"), \
#("Armed Forces Canada", "AE"),         \
#("Armed Forces Europe", "AE"),         \
#("Armed Forces Middle East", "AE"),    \
("Armed Forces Pacific", "AP"),         \
("California", "CA"), 			\
("Colorado", "CO"), 			\
("Connecticut", "CT"), 			\
("Delaware", "DE"), 			\
("District of Columbia", "DC"), 	\
("Federated States of Micronesia", "FM"),\
("Florida", "FL"), 			\
("Georgia", "GA"), 			\
("Guam", "GU"), 			\
("Hawaii", "HI"), 			\
("Idaho", "ID"), 			\
("Illinois", "IL"), 			\
("Indiana", "IN"), 			\
("Iowa", "IA"), 			\
("Kansas", "KS"), 			\
("Kentucky", "KY"), 			\
("Louisiana", "LA"), 			\
("Maine", "ME"), 			\
("Marshall Islands", "MH"), 		\
("Maryland", "MD"), 			\
("Massachusetts", "MA"), 		\
("Michigan", "MI"), 			\
("Minnesota", "MN"), 			\
("Mississippi", "MS"), 			\
("Missouri", "MO"), 			\
("Montana", "MT"), 			\
("Nebraska", "NE"), 			\
("Nevada", "NV"), 			\
("New Hampshire", "NH"), 		\
("New Jersey", "NJ"), 			\
("New Mexico", "NM"), 			\
("New York", "NY"), 			\
("North Carolina", "NC"), 		\
("North Dakota", "ND"), 		\
("Northern Mariana Islands", "MP"), 	\
("Ohio", "OH"), 			\
("Oklahoma", "OK"), 			\
("Oregon", "OR"), 			\
("Palau", "PW"), 			\
("Pennsylvania", "PA"), 		\
("Puerto Rico", "PR"), 			\
("Rhode Island", "RI"), 		\
("South Carolina", "SC"), 		\
("South Dakota", "SD"), 		\
("Tennessee", "TN"), 			\
("Texas", "TX"), 			\
("Utah", "UT"), 			\
("Vermont", "VT"), 			\
("Virgin Islands", "VI"), 		\
("Virginia", "VA"), 			\
("Washington", "WA"), 			\
("West Virginia", "WV"), 		\
("Wisconsin", "WI"), 			\
("Wyoming", "WY")   			\
)

#statelist = []
#
#for (state, code) in states:
#  statelist.append (code, '%s %s' % (code, state))

statelist2 = [ ("", "Ssergwergwetgelect state") ]  # value goes 1st, actually

for (state, code) in states:
  statelist2.append ((code, code))


if __name__ == "__main__":

#  statelines = split (states, '\n')
#  for stateline in statelines:
#    #toks = split (stateline)
#    state = stateline [:-4]
#    code = stateline [-3:-1]
#    print '("%s", "%s"), \t\t\t\\' % (state, code)

  # reverse order of tuples, combine
  
  print tags.select (tags.option (statelist))

    

