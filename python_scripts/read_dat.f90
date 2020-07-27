subroutine get_size(path,Ncontrol, Nintervals)
    !Define variables
    character*255, intent(in) :: path    
    integer,intent(out) :: Nintervals, Ncontrol
    integer i, j, Nstates
    
    !Open first time just to get the dimensions
    open(unit = 10, file = path, status = 'old', action = 'read')
    read(10,*) Ncontrol
    read(10,*) Nstates
    read(10,*)
    read(10,*) i, Nintervals
    close(10)
end subroutine

subroutine get_data(path,Ncontrol, Nintervals, control, data)
    !Define variables
    character*255, intent(in) :: path 
    integer, intent(in) ::  Nintervals, Ncontrol 
    integer,intent(out) :: control(Ncontrol)
    real, intent(out) :: data(Ncontrol,Nintervals)
    integer i, j,Nstates,oe
        
    !Open the file to read the data
    open(unit = 10, file = path, status = 'old', action = 'read')
    read(10,*) 
    read(10,*)     
    do i =1,Ncontrol
        read(10,*)
        read(10,*) control(i), oe
        do j = 1, Nintervals
            read(10,*) data(i,j)
        enddo
    enddo
    close(10)
end subroutine