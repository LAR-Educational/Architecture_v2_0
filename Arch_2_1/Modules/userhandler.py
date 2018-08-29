import os


class UserDatabase():

    def __init__(self):
        print "HI 2"
        self.path = "Usuarios/"
        print os.listdir(self.path)


    def load_users(self):
        pass



class User():

    def __init__(self, id, first_name, last_name='None', bday='None',
                 scholl_year='None', picture='None', preferences='None'):
        
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.bday=bday
        self.scholl_year=scholl_year
        self.picture=picture
        self.preferences=preferences
        
                     




    def setPreferences(self, sport='None', team='None', toy='None', game='None', 
                        dance='None', music='None', hobby='None', food='None'):
        self.preferences['sport']=sport
        self.preferences['team']=team
        self.preferences['toy']=toy
        self.preferences['game']=game
        self.preferences['dance']=dance
        self.preferences['music']=music
        self.preferences['hobby']=hobby
        self.preferences['food']=food



def main():

    print "HI 1"
    userdatabase = UserDatabase()



if __name__=='__main__':
    main()          