'''
Name    : Rupesh Garsondiya 
github  : @Rupeshgarsondiya
Topic   : Fitness Model (Computer Vision)
Organization : L.J University
'''

import Fiteness_Model_Cv as fm
from Fiteness_Model_Cv import CalAngle,Dumbbell_Forearm_Curl,Arm_Raises,Side_Arm_Raise,Squats,BackWard_Lunge

mp_drawing = fm.mp_drawing
mp_pose = fm.mp_pose

while True :

    print('Enter 1 for the Dumbbell Forearm Curl')
    print('Enter 2 for the Arm Raises')
    print('Enter 3 for side arm raise')
    print('Enter 4 for Squats')
    print("Enter 5 for Backward Lunge")
    print('Enter 6 for the Exit')

    try:
        choice = int(input('Enter your choice: '))
        if choice == 1:
            Dumbbell_Forearm_Curl()
        elif choice == 2:
            Arm_Raises()
        elif choice == 3:
            Side_Arm_Raise()
        elif choice == 4:
            Squats()
        elif choice == 5:
            BackWard_Lunge()
        elif choice == 6:
            print('Exiting the program')
            break;
        else:
            print('Invalid choice')
    except ValueError:
        print('Invalid choice. Please enter a number.')