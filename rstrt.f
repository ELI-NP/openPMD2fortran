      program main
      IMPLICIT NONE
      INTEGER, PARAMETER :: icpu=16
      INTEGER :: iteration,dimensions,L,LP,IPTSS,IPTFF,Lall
      REAL(kind=8), DIMENSION(:), ALLOCATABLE :: x,y
        
      OPEN(1, file="restrt189600.dat" , form='unformatted')
      OPEN(2, file="pospic189600.dat" , form='formatted')
    
      READ(1) iteration
      READ(1) dimensions

      WRITE(*,*) iteration, dimensions

      ALLOCATE(x(dimensions))
      ALLOCATE(y(dimensions))

      READ(1) x
      READ(1) y
      CLOSE(1)

      Lall = int(dimensions/icpu)
      DO LP = 1,icpu
        IPTSS  = Lall*(LP-1)+1
        IPTFF  = Lall*LP
      DO L  = IPTSS,IPTFF
        WRITE(2,*) x(L), y(L)
      END DO
      END DO
      CLOSE(2)
      STOP
      END