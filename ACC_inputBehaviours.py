def input_restrict(self):
      print('')
      print("Choose an index (int), 'modify', or 'quit'")
        
      while True:
            temp = input()
                  
            # if a digit, send back as an int
            if temp.isdigit():

                 return int(temp)

            
            elif temp == 'modify':
                  # will return aDict or 'quit'
                  return self.modifySubmission()

                  #self.returnBack_clean = results
                      
                  # handle where this goes after modifySubmission
                  # this needs to reload 'Addresses Completed' and the new submission
                      
            elif temp == 'quit':
                  print('\t', 'You quit the process. You must start over.')
                  return temp
            else:
                  print('\t', 'Invalid entry, try again...')

def input_reg(self):
      print('')
      print("Choose an index (int), move 'back', 'modify', or 'quit'")
        
      while True:
            temp = input()
                  
            # if a digit, send back as an int
            if temp.isdigit():
                  return int(temp)
                  
            # if 'back', pop the last item in df_list and redisplay df_list
            elif temp == 'back':

                  # handle pop() for empty lists
                      
                  self.goBack()
                  return self.selectCell()
                   
                  
            elif temp == 'modify':
                  # will return aDict or 'quit'
                  return self.modifySubmission()

                  #self.returnBack_clean = results
                      
                  # handle where this goes after modifySubmission
                  # this needs to reload 'Addresses Completed' and the new submission
                      
            elif temp == 'quit':
                  print('\t', 'You quit the process. You must start over.')
                  return temp
            else:
                  print('\t', 'Invalid entry, try again...')

def input_boleanReturn(text):

      while True:
            print(text)
            temp = input()

            if temp == 'yes':
                  return True
            elif temp == 'quit':
                  return False
            else:
                print('Invalid entry, try again')

def inputThree(text):

        while True:
            print(text)
            temp = input()

            if temp == 'yes':
                return True
            elif temp == 'quit':
                return False
                break
            else:
                print('Invalid entry, try again')










                
