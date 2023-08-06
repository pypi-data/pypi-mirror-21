c compile with: f2py -c -m fortran fortran.f
c
      function f(x, n)
      integer i
      real*8 x(n), x2, f
      x2 = 0.0
      do i=1,n
        x2 = x2 + (x(i) - 0.3333333) ** 2
      end do
      f= exp(-100. * x2) * (sqrt(100./3.141592654d0)**n)
      return
      end
