from random import randint

def generator(n: int):
    matrice = []
    for i in range(n):
        matrice.append(list(range(n)))
    
    for i in range(n):
        for j in range(n):
            if i == j:
                matrice[i][j] = 0
            elif j > i :
                matrice[i][j] = matrice[j][i]
            else:   
                matrice[i][j] = randint(1, 100)

    for i in range(n):
        for j in range(n):
            if i == j:
                matrice[i][j] = 0
            elif i > j :
                matrice[i][j] = matrice[j][i]
            else:   
                matrice[i][j] = randint(1, 100)
    with open("data.txt", 'w') as file :
        for i in range(n):
            file.writelines(str(matrice[i]))
            file.write('\n')
    return matrice

#printgenerator(11))