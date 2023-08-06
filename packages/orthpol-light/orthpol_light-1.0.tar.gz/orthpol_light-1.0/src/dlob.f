c
c

      subroutine dlob(n,dalpha,dbeta,dleft,dright,dzero,dweigh,
     *ierr,de,da,db)
c
c This is a double-precision version of the routine  lob.
c
      double precision dleft,dright,dp0l,dp0r,dp1l,dp1r,dpm1l,
     *dpm1r,ddet,dalpha,dbeta,dzero,dweigh,de,da,
     *db
      dimension dalpha(n),dbeta(n),dzero(n+2),dweigh(n+2),
     *de(n+2),da(n+2),db(n+2)
c
c The arrays  dalpha,dbeta,dzero,dweigh,de,da,db  are assumed to have
c dimension  n+2.
c
cf2py integer intent(hide),depend(dalpha) :: n=len(dalpha)
cf2py double precision intent(in) :: dalpha
cf2py double precision intent(in),depend(n),dimension(n) :: dbeta
cf2py double precision intent(in) :: dleft
cf2py double precision intent(in) :: dright
cf2py double precision intent(out),depend(n),dimension(n+2) :: dzero
cf2py double precision intent(out),depend(n),dimension(n+2) :: dweigh
cf2py integer intent(out) :: ierr
cf2py double precision intent(hide),depend(n),dimension(n+2) :: de
cf2py double precision intent(hide),depend(n),dimension(n+2) :: da
cf2py double precision intent(hide),depend(n),dimension(n+2) :: db
      np1=n+1
      np2=n+2
      do 10 k=1,np2
        da(k)=dalpha(k)
        db(k)=dbeta(k)
   10 continue
      dp0l=0.d0
      dp0r=0.d0
      dp1l=1.d0
      dp1r=1.d0
      do 20 k=1,np1
        dpm1l=dp0l
        dp0l=dp1l
        dpm1r=dp0r
        dp0r=dp1r
        dp1l=(dleft-da(k))*dp0l-db(k)*dpm1l
        dp1r=(dright-da(k))*dp0r-db(k)*dpm1r
   20 continue
      ddet=dp1l*dp0r-dp1r*dp0l
      da(np2)=(dleft*dp1l*dp0r-dright*dp1r*dp0l)/ddet
      db(np2)=(dright-dleft)*dp1l*dp1r/ddet
      call dgauss(np2,da,db,dzero,dweigh,ierr,de)
      return
      end

