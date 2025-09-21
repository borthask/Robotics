# main
def trapezoidal_motion_profile(distance, v_max, a_max, dt=0.01, pl=True):
    # Time and distance to accelerate/decelerate
    t_acc = v_max / a_max
    d_acc = 0.5 * a_max * t_acc**2

    # Ensure we can reach max velocity
    if 2 * d_acc > distance:
        raise ValueError("Distance too short to reach v_max with given acceleration.")

    # Cruise phase
    d_cruise = distance - 2 * d_acc
    t_cruise = d_cruise / v_max

    # Total time and time vector
    t_total = 2 * t_acc + t_cruise
    t = np.arange(0, t_total + dt, dt)

    # Allocate arrays
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    a = np.zeros_like(t)

    for i in range(len(t)):
        ti = t[i]
        if ti < t_acc:
            # Acceleration phase
            a[i] = a_max
            v[i] = a_max * ti
            x[i] = 0.5 * a_max * ti**2
        elif ti < t_acc + t_cruise:
            # Cruise phase
            a[i] = 0
            v[i] = v_max
            x[i] = d_acc + v_max * (ti - t_acc)
        else:
            # Deceleration phase
            td = ti - (t_acc + t_cruise)
            a[i] = -a_max
            v[i] = v_max - a_max * td
            x[i] = d_acc + d_cruise + v_max * td - 0.5 * a_max * td**2
    
    if pl==True:
            # Plotting
        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.plot(t, x, label='Position (m)')
        plt.ylabel('Position')
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.plot(t, v, label='Velocity (m/s)', color='green')
        plt.ylabel('Velocity')
        plt.grid(True)

        plt.subplot(3, 1, 3)
        plt.plot(t, a, label='Acceleration (m/s²)', color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration')
        plt.grid(True)

        plt.tight_layout()
        plt.show()
        

    return t, x, v, a


def compute_motor_current(acc, time, J, kt, T_load=None):
    """
    Compute DC motor current from acceleration profile.

    Parameters:
    - acc: acceleration array (rad/s² or m/s² if linear)
    - time: time array (s)
    - J: system inertia (kg·m² or kg)
    - kt: torque constant (Nm/A)
    - T_load: optional load torque array (Nm)

    Returns:
    - current: estimated current array (A)
    """
    if T_load is None:
        T_load = np.zeros_like(acc)

    torque = J * acc + T_load
    current = torque / kt
    return current, torque

 
def compute_motor_losses(current,v,time,rho,num_motors,hys_eta,pl=True):
    """
    Compute DC motor losses  from current profile and other input parameters.
    Parameters:
    - current: current array (amps)
    - time: time array (s)

    Returns:
    - current: estimated motor losses
    """
    copper_loss = rho * current**2*num_motors
    iron_loss =hys_eta*num_motors*v

    if pl==True:
        
        plt.figure(figsize=(10, 5))
        plt.subplot(3, 1, 1)
        plt.plot(t, torque, label='Torque (Nm)')
        #plt.plot(t, stall_torque*np.ones_like(t), label='Stall Torque (Nm)')
        plt.ylabel('Torque')
        plt.legend()

        plt.grid()

        plt.subplot(3, 1, 2)
        plt.plot(t, current, label='Current (A)', color='r')
        plt.xlabel('Time (s)')
        plt.ylabel('Current')
        plt.grid()

        plt.subplot(3, 1, 3)
        plt.plot(t, copper_loss, label='Copper_Loss', color='red')
        plt.plot(t, iron_loss, label='Iron_Loss', color='green')
        plt.plot(t, iron_loss+copper_loss, label='Total Loss', color='blue')
        plt.xlabel('Time (s)')
        plt.ylabel('Watts')
        plt.legend()

        plt.grid()


        plt.tight_layout()
        
        plt.show()
    return copper_loss, iron_loss


def animate(t,start_coord,end_coord,pts,filename):

    # Set up the figure and axis
    t1=np.linspace(t[0],t[-1],pts)
    x1=np.linspace(start_coord[0],end_coord[0],pts)
    y1=np.linspace(start_coord[1],end_coord[1],pts)
    fig, axis=plt.subplots()
    axis.set_xlim([min(x1),max(x1)])
    axis.set_ylim([min(y1),max(y1)])



    animated_plot,=axis.plot([],[])


    def update_data(frame):
        animated_plot.set_data(x1[:frame],y1[:frame])
        return animated_plot,

    animation=FuncAnimation(fig=fig,func=update_data,frames=len(t1),interval=10)
    animation.save(filename)

def projectile_motion_profile(v_init,angle, dt=0.005, pl=True):
    import math as m
    
    angle_radians = m.radians(angle)
    gravity=9.81
    
    # Total time and time vector
    t_total = 2 * v_init * m.sin(angle_radians)/gravity
    t = np.arange(0, t_total + dt, dt)
    
    #initualize the arrays
    x=np.zeros_like(t)
    y=np.zeros_like(t)

    
    for i in range(len(t)):
          ti = t[i]
          # Acceleration phase
          y[i] = v_init*m.sin(angle_radians)*ti-0.5*gravity*ti**2
          x[i] = v_init*m.cos(angle_radians)*ti

          if y[i]<=0:
                y[i] = 0
                x[i]=x[i]
            
       
    # this is the range ( max x ) and ht (max y) 
    
    ran=v_init**2*m.sin(2*angle_radians)/gravity
    ht=v_init**2*m.sin(angle_radians)**2/(2*gravity)

    if pl==True:
            # Plotting
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='Position (m)')
        plt.ylabel('Position')
        plt.grid(True)

        plt.tight_layout()
        plt.show()
        

    return t, x, y, ran,ht
