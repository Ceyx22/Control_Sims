from sympy import * 

m = Symbol('m') # mass of leg
M = Symbol('M') # mass of hip
I = Symbol('I') # Inertia
c = Symbol('c') # Center of mass of leg from hip joint
l = Symbol('l') # length of leg
theta1 = Symbol('theta_1') # absolute angle
theta2 = Symbol('theta_2')  # angle between stance and swing leg
theta1_n = Symbol('theta1_n')
theta2_n = Symbol('theta2_n') #angles before heelstrike

x = Symbol('x')  # x position of stance leg
y = Symbol('y')  # y position of stance leg

#Angular velocity
omega1 = Symbol('omega1')
omega2 = Symbol('omega2')

# velocity of the stance leg
vx = Symbol('vx')
vy = Symbol('vy') 


gamma = Symbol('gamma') # Slope of ramp
gravity = Symbol('gravity')  # gravity

# acceleration of the stance leg
ax = Symbol('ax') 
ay = Symbol('ay') 

# Angular Acceleration
alpha1 = Symbol('alpha1')
alpha2 = Symbol('alpha2')

# Position Vectors
# angle made by frame 0 with frame 1
R01 = Matrix([
    [cos(pi/2+theta1), -sin(pi/2+theta1)],
    [sin(pi/2+theta1),  cos(pi/2+theta1)]
    ])
# angle made by frame 1 with frame 2
R12 = Matrix([
    [cos(-pi+theta2), -sin(-pi+theta2)],
    [sin(-pi+theta2),  cos(-pi+theta2)]
    ])
# position of c1 with respect to frame 0
RC1 = Matrix([x,y])
# position of O1 with respect to frame 0
O01 = Matrix([x,y])
# position of O1 with respect to frame 0
O12 = Matrix([l, 0])
# Homogonous transformations
H01 = Matrix([ [R01, O01], [0, 0, 1] ])
H12 = Matrix([ [R12, O12], [0, 0, 1] ])

R_H = H01*Matrix([l, 0, 1])
x_H = Matrix([R_H[0]])
y_H = Matrix([R_H[1]])


R_G1 = H01*Matrix([(l-c), 0, 1])
x_G1 = Matrix([R_G1[0]])
y_G1 = Matrix([R_G1[1]])

R_G2 = H01*H12*Matrix([c, 0, 1])
r_G2 = simplify(R_G2)
x_G2 = Matrix([r_G2[0]])
y_G2 = Matrix([r_G2[1]])

R_C2 = H01*H12*Matrix([l, 0, 1])
r_C2 = simplify(R_C2)
x_C2 = Matrix([r_C2[0]])
y_C2 = Matrix([r_C2[1]])

# Velocity Vectors
vel_vect = Matrix([vx, vy, omega1, omega2])
deriv_vect = Matrix([x, y, theta1, theta2])
v_H_x = x_H.jacobian(deriv_vect) * vel_vect
v_H_y = y_H.jacobian(deriv_vect) * vel_vect
v_G1_x = x_G1.jacobian(deriv_vect) * vel_vect
v_G1_y = y_G1.jacobian(deriv_vect) * vel_vect
v_G2_x = x_G2.jacobian(deriv_vect) * vel_vect
v_G2_y = y_G2.jacobian(deriv_vect) * vel_vect
v_H = simplify(Matrix([v_H_x, v_H_y]))
v_G1 = simplify(Matrix([v_G1_x, v_G1_y]))
v_G2 = simplify(Matrix([v_G2_x, v_G2_y]))

# Position Vectors for Potentail Energy
# Get positions of masses with respect to the global frame
R = simplify(Matrix([
    [cos(-gamma), -sin(-gamma)],
    [sin(-gamma),  cos(-gamma)]
    ]))

R_H = simplify(R*Matrix([x_H, y_H]))
R_G1 = simplify(R*Matrix([x_G1, y_G1]))
R_G2 = simplify(R*Matrix([x_G2, y_G2]))

Y_H = R_H[1]
Y_G1 = R_G1[1]
Y_G2 = R_G2[1]

# Potential, Kinetic, and Total Energy
T = 0.5*(simplify(m*(v_G1.dot(v_G1)) + m*(v_G2.dot(v_G2)) + M*(v_H.dot(v_H) ) + I*(Pow(omega1, 2) + Pow(omega1+omega2, 2)) ))
# potential is positive because com is above reference point
V = simplify(m*gravity*Y_G1+m*gravity*Y_G2+M*gravity*Y_H)
L = T-V

# equations of motion
q = Matrix([x, y, theta1, theta2])
qdot = Matrix([vx, vy, omega1, omega2])
qddot = Matrix([ax, ay, alpha1, alpha2])
EOM = Matrix()
for i in range(4):
    dLdqdot = diff(L,qdot[i])
    ddt_dLdqdot = diff(dLdqdot,q[0])*qdot[0] + diff(dLdqdot,qdot[0])*qddot[0]+ diff(dLdqdot,q[1])*qdot[1] + diff(dLdqdot,qdot[1])*qddot[1]+ diff(dLdqdot,q[2])*qdot[2] + diff(dLdqdot,qdot[2])*qddot[2]+ diff(dLdqdot, q[3])*qdot[3] + diff(dLdqdot,qdot[3])*qddot[3]
    dLdq = diff(L,q[i])
    EOM = EOM.row_insert(i, Matrix([ddt_dLdqdot - dLdq]))

# here A_ss is floating base 
b_ss = Matrix()
zero_vect = Matrix([0, 0, 0, 0])
A_ss = EOM.jacobian(qddot)
b_ss = b_ss.row_insert(0, Matrix([-EOM[0].subs([(qddot[0],zero_vect[0]), (qddot[1],zero_vect[1]), (qddot[2],zero_vect[2]), (qddot[3],zero_vect[3])])]))
b_ss = b_ss.row_insert(1, Matrix([-EOM[1].subs([(qddot[0],zero_vect[0]), (qddot[1],zero_vect[1]), (qddot[2],zero_vect[2]), (qddot[3],zero_vect[3])])]))
b_ss = b_ss.row_insert(2, Matrix([-EOM[2].subs([(qddot[0],zero_vect[0]), (qddot[1],zero_vect[1]), (qddot[2],zero_vect[2]), (qddot[3],zero_vect[3])])]))
b_ss = b_ss.row_insert(3, Matrix([-EOM[3].subs([(qddot[0],zero_vect[0]), (qddot[1],zero_vect[1]), (qddot[2],zero_vect[2]), (qddot[3],zero_vect[3])])]))

# We only use the elements from alpha1 and alpha2 (row, columns 2 and 3)
print('ss equations start here')
print(f'A11 = {simplify(A_ss[2,2])}')
print(f'A12 = {simplify(A_ss[2,3])}')
print(f'A21 = {simplify(A_ss[3,2])}')
print(f'A22 = {simplify(A_ss[3,3])}')
print('A_ss = Matrix([A11, A12, A21, A22])')
print(' ')
print(f'b1 = {simplify(b_ss[2])}')
print(f'b2 = {simplify(b_ss[3])}')
print('b_ss = Matrix([b1, b2])')
print(' ')
print('alpha = A_ss \ b_ss')
print(' ')
print(' ')

j = Matrix([x_C2, y_C2])
J_sw =  j.jacobian(q)
J_n_sw = J_sw.subs([(theta1, theta1_n), (theta2, theta2_n)])
A_n_hs = A_ss.subs([(theta1, theta1_n), (theta2, theta2_n)])

print(' ')
print('foot strike equations start here')
print(' ')

print(f'J11 = {simplify(J_n_sw[0,0])}')
print(f'J12 = {simplify(J_n_sw[0,1])}')
print(f'J13 = {simplify(J_n_sw[0,2])}')
print(f'J14 = {simplify(J_n_sw[0,3])}')
print(f'J21 = {simplify(J_n_sw[1,0])}')
print(f'J22 = {simplify(J_n_sw[1,1])}')
print(f'J23 = {simplify(J_n_sw[1,2])}')
print(f'J24 = {simplify(J_n_sw[1,3])}')
print('J = Matrix([[J11, J12, J13, J14], [J21, J22, J23, J24]])')
print(' ')

print(f'A11 = {simplify(A_n_hs[0,0])}')
print(f'A12 = {simplify(A_n_hs[0,1])}')
print(f'A13 = {simplify(A_n_hs[0,2])}')
print(f'A14 = {simplify(A_n_hs[0,3])}')

print(f'A21 = {simplify(A_n_hs[1,0])}')
print(f'A22 = {simplify(A_n_hs[1,1])}')
print(f'A23 = {simplify(A_n_hs[1,2])}')
print(f'A24 = {simplify(A_n_hs[1,3])}')

print(f'A31 = {simplify(A_n_hs[2,0])}')
print(f'A32 = {simplify(A_n_hs[2,1])}')
print(f'A33 = {simplify(A_n_hs[2,2])}')
print(f'A34 = {simplify(A_n_hs[2,3])}')

print(f'A41 = {simplify(A_n_hs[3,0])}')
print(f'A42 = {simplify(A_n_hs[3,1])}')
print(f'A43 = {simplify(A_n_hs[3,2])}')
print(f'A44 = {simplify(A_n_hs[3,3])}')
print('A_n_hs = Matrix([A11, A12, A13, A14, A21, A22, A23, A24, A31, A32, A33, A34, A41, A42, A43, A44])')
print(' ')

print('X_n_hs = Matrix([0, 0, omega1_n, omega2_n])') # [vx_stance vy_stance omega1 omega2]
print('b_hs = Matrix([A_n_hs*X_n_hs, 0, 0])') # [momentum before footstrike = A_n_hs*X_n_hs v_swing_foot_after_foot_strike = 0 0 
print('A_hs = Matrix([[A_n_hs, -J],  [J, zeros(2,2)]])')
print('X_hs = A_hs \ b_hs')
print('omega(1) = X_hs[2]+X_hs[3]')
print('omega[1] = -X_hs[3]')
print(' ')