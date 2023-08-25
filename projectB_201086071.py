import sys
import numpy as np
import matplotlib.pylab as plt

def output_file():

    x = ["-2", "0", "2", "4", "6"]

    y = ["2.1", "2.4", "2.5", "3.5", "4.2"]

    error = open('random.dat', 'r')

    error_list = []

    for line in error:
    
        error_list.append(line)

        if(line == '0' or line == '0.0'):
            
            sys.exit("Error values contain 0")
            
    n = 0
        
    if (len(x) != len(y)):
            
        sys.exit('x or y data error')
        
    with open('project_B_data', 'wt') as output_file:
    
        while (n < len(x)):
        
            data = []

            x_val = str(x[n])
        
            data.append(x_val)
            data.append(", ")
        
            y_val = str(y[n])
        
            data.append(y_val)
            data.append(", ")
        
            error_val = str(error_list[n])
        
            data.append(error_val)
        
            output_file.writelines(data)

            n = n + 1
            
    if (len(x) != len(error_list)):
            
        sys.exit('File syntax error')
            
def read_to_numpy_arr():
    
    try:
    
        overall_list = open('project_B_data', 'r')
    
    except:
        
        sys.exit("File not found!")
        
    x_list = []
    y_list = []
    error_list = []
    line_count = 0
    
    for line in overall_list:
    
        line_list = list(line)
        comma_count = 0

        x_chars = []
        y_chars = []
        error_chars = []
        
        for char in line_list:
            
            if(comma_count == 0):
                
                if((ord(char) <= 57 and ord(char) >= 48) or ord(char) == 45 or ord(char) == 46):
                    
                    x_chars.append(char)
                    
                elif(ord(char) == 44):
                    
                    comma_count += 1
                    
            elif(comma_count == 1):
                
                if((ord(char) <= 57 and ord(char) >= 48) or ord(char) == 45 or ord(char) == 46):
                    
                    y_chars.append(char)
                    
                elif(ord(char) == 44):
                    
                    comma_count += 1
                    
            elif(comma_count == 2):
            
                if((ord(char) <= 57 and ord(char) >= 48) or ord(char) == 45 or ord(char) == 46):
                    
                    error_chars.append(char)
                    
            elif((ord(char) >= 57 and ord(char) <= 48) or ord(char) != 45 or ord(char) != 46):
                
                sys.exit("Incorrect syntax in file!")
                    
        line_count += 1
        
        if(comma_count != 2):
        
            sys.exit("File content error, 3 points of data needed in a set!")
         
        x_index = "".join(x_chars)
        y_index = "".join(y_chars)
        error_index = "".join(error_chars)
        
        x_list.append(x_index)
        y_list.append(y_index)
        error_list.append(error_index)
    
    if(line_count != 5):
        
        sys.exit("File content error, 5 sets of data not present!")
    
    x_arr = np.asarray(x_list).astype(np.float)
    y_arr = np.asarray(y_list).astype(np.float)
    error_arr = np.asarray(error_list).astype(np.float)
    val_calculation(x_arr, y_arr, error_arr)
    draw_graph(x_arr, y_arr, error_arr)
        
def val_calculation(x_arr, y_arr, error_arr):
    
    p = 0
    q = 0
    r = 0
    s = 0
    t = 0
    n = 0
    
    for n in range(0,5):
        
        p = p + (1/float(error_arr[n])**2)
        q = q + (float(x_arr[n])/float(error_arr[n])**2)
        r = r + (float(y_arr[n])/float(error_arr[n])**2)
        s = s + (float(x_arr[n])**2/float(error_arr[n])**2)
        t = t + (float(x_arr[n])*float(y_arr[n])/float(error_arr[n])**2)
    
    delta = (p*s) - q**2
    
    least_square_values(p, q, r, s, t, delta)

def least_square_values(p, q, r, s ,t, delta):
    
    a_top = (r*s) - (q*t)
    b_top = (p*t) - (q*r)
    
    a = format(a_top/delta, '.4f')
    b = format(b_top/delta, '.4f')
    
    sigma_a = format((s/delta)**0.5, '.6f')
    sigma_b = format((p/delta)**0.5, '.6f')

    print("a = "+str(a)+", b = "+str(b)+", a uncertainty = "+str(sigma_a)+", b uncertainty = "+str(sigma_b))
    
def draw_graph(x_arr, y_arr, error_arr):
    
    new_error_arr = []
    count = 1
    
    for n in error_arr:
        
        new_error_arr.append(str(count)+': '+str(format(n, '.3f')))
        count += 1
    
    error_vals = " ".join(new_error_arr)
    
    slope, intercept = np.polyfit(x_arr, y_arr, 1)
    gradient = str(slope)
    plt.plot(np.unique(x_arr), np.poly1d(np.polyfit(x_arr, y_arr, 1))(np.unique(x_arr)), label = 'Line gradient = '+gradient+'\nError values: '+error_vals)
    
    x_margin = (max(x_arr) - min(x_arr))*0.1
    y_margin = (max(y_arr) - min(y_arr) + max(error_arr))*0.2
    
    plt.axis([(min(x_arr)-x_margin), (max(x_arr)+x_margin), (min(y_arr)-y_margin), (max(y_arr)+y_margin)])
    plt.errorbar(x_arr, y_arr, yerr = error_arr, fmt= 'x')
    
    plt.xlabel("x data")
    plt.ylabel("y data")
    plt.title("Student ID data")
    
    plt.legend(bbox_to_anchor=(0.8, 0.85), bbox_transform=plt.gcf().transFigure, fontsize = 9, handlelength = 0)
    
    plt.show()

output_file()
read_to_numpy_arr()

sys.exit("Programme finished")