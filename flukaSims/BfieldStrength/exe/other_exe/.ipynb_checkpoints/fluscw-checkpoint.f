*                                                                      *
*=== fluscw ===========================================================*
*                                                                      *
      DOUBLE PRECISION FUNCTION FLUSCW ( IJ    , PLA   , TXX   , TYY   ,
     &                                   TZZ   , WEE   , XX    , YY    ,
     &                                   ZZ    , NREG  , IOLREG, LLO   ,
     &                                   NSURF )

      INCLUDE 'dblprc.inc'
      INCLUDE 'dimpar.inc'
      INCLUDE 'iounit.inc'
      INCLUDE 'trackr.inc'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 2003-2019:  CERN & INFN                            *
*     All Rights Reserved.                                             *
*                                                                      *
*     New version of Fluscw for FLUKA9x-FLUKA20xy:                     *
*                                                                      *
*     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     *
*     !!! This is a completely dummy routine for Fluka9x/20xy. !!!     *
*     !!! The  name has been kept the same as for older  Fluka !!!     *
*     !!! versions for back-compatibility, even though  Fluscw !!!     *
*     !!! is applied only to estimators which didn't exist be- !!!     *
*     !!! fore Fluka89.                                        !!!     *
*     !!! User  developed versions  can be used for  weighting !!!     *
*     !!! flux-like quantities at runtime                      !!!     *
*     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     *
*                                                                      *
*     Input variables:                                                 *
*                                                                      *
*           Ij = (generalized) particle code (Paprop numbering)        *
*          Pla = particle laboratory momentum (GeV/c) (if > 0),        *
*                or kinetic energy (GeV) (if <0 )                      *
*    Txx,yy,zz = particle direction cosines                            *
*          Wee = particle weight                                       *
*     Xx,Yy,Zz = position                                              *
*         Nreg = (new) region number                                   *
*       Iolreg = (old) region number                                   *
*          Llo = particle generation                                   *
*        Nsurf = transport flag (ignore!)                              *
*                                                                      *
*     Output variables:                                                *
*                                                                      *
*       Fluscw = factor the scored amount will be multiplied by        *
*       Lsczer = logical flag, if true no amount will be scored        *
*                regardless of Fluscw                                  *
*                                                                      *
*     Useful variables (common SCOHLP):                                *
*                                                                      *
*     Flux like binnings/estimators (Fluscw):                          *
*          ISCRNG = 1 --> Boundary crossing estimator                  *
*          ISCRNG = 2 --> Track  length     binning                    *
*          ISCRNG = 3 --> Track  length     estimator                  *
*          ISCRNG = 4 --> Collision density estimator                  *
*          ISCRNG = 5 --> Yield             estimator                  *
*          JSCRNG = # of the binning/estimator                         *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE 'scohlp.inc'
*
************************************************************************
*     ! Particle Dumping Routine
*     ! Created by Fabio Pozzi - HSE-RP at CERN
*     ! 
*     ! Dumps relevant information for particle types defined in the
*     ! corresponding USRBDX card.
*     ! 
*     ! Version 1 – April 2019
*     ! Version 2 – February 2020 (by Alajos Makovec – HSE-RP at CERN)
*     ! Version 3 – June 2025 (by Alajos Makovec – RadSim at Fermilab)
************************************************************************
*     ! Activated using a USERWEIGHT card in Flair:
*     !   - Select "FLUSCW+" as weight
*     !   - Select "No weight" for residual nuclei
*     !   - Leave empty Density Weight (no selection)
*     ! 
*     ! Checks if the estimator is a boundary crossing estimator
*     ! using ISCRNG (see lines 52 to 57).
*     ! 
*     ! Limits dumping to selected estimators of interest, for example:
*     ! First estimator: 
*     ! IF (ISCRNG .EQ. 1 .AND. JSCRNG .EQ. 1) THEN
*     ! Fifth estimator:
*     ! IF (ISCRNG .EQ. 1 .AND. JSCRNG .EQ. 5) THEN
*     ! First and fifth:
*     ! IF (ISCRNG .EQ. 1 .AND. (JSCRNG .EQ. 1 .OR. JSCRNG .EQ. 5)) THEN
*     ! All boundary crossing estimators:
*     ! IF (ISCRNG .EQ. 1) THEN
************************************************************************
      LOGICAL LFIRST1           ! Logical flag to track first execution
      DATA LFIRST1 / .TRUE. /   ! Initialize LFIRST to TRUE
      SAVE LFIRST1              ! Preserve value of LFIRST between calls
      
      LOGICAL LFIRST2
      DATA LFIRST2 / .TRUE. /
      SAVE LFIRST2
      
      LOGICAL LFIRST3
      DATA LFIRST3 / .TRUE. /
      SAVE LFIRST3
      
      LOGICAL LFIRST4
      DATA LFIRST4 / .TRUE. /
      SAVE LFIRST4

      ! Variables used to create EVENT_COUNT
      DOUBLE PRECISION LAST_TPROD, LAST_TARO
      DATA LAST_TPROD /0.0D0/
      DATA LAST_TARO /0.0D0/
      SAVE LAST_TPROD, LAST_TARO

      ! gives the event number of every particle recorded
      INTEGER EVENT_COUNT, PID
      DATA EVENT_COUNT /0/
      DATA PID /0/
      SAVE EVENT_COUNT, PID

      ! Variables used to calculate kinetic energy (for USRYIELD) 
      ! and momentum (for USRBDX)
      DOUBLE PRECISION MASS, EKIN, MOM
      DATA MASS /0.0D0/
      DATA EKIN /0.0D0/
      DATA MOM /0.0D0/
      SAVE MASS, EKIN, MOM      

      FLUSCW = ONEONE           ! See line 45
      LSCZER = .FALSE.          ! See lines 46 to 47

      IF ( LFIRST1 ) THEN
         LFIRST1 = .FALSE.
         OPEN(UNIT=99, FILE='prod.txt', STATUS='UNKNOWN')
         WRITE(99,9999) "# ID", "E_kin[GeV]", "P[GeV]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]",
     &        "Gen", "Evnt", "pid"
      END IF
 9999 FORMAT (A6,9A15,2A10,A6)

      IF ( LFIRST2 ) THEN
         LFIRST2 = .FALSE.
         OPEN(UNIT=98, FILE='esc.txt', STATUS='UNKNOWN')
         WRITE(98,9888) "# ID", "E_kin[GeV]", "P[GeV]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]",
     &        "Gen", "Evnt", "pid"
      END IF
 9888 FORMAT (A6,9A15,2A10,A6)

      IF ( LFIRST3 ) THEN
         LFIRST3 = .FALSE.
         OPEN(UNIT=97, FILE='det1.txt', STATUS='UNKNOWN')
         WRITE(97,9777) "# ID", "E_kin[GeV]", "P[GeV]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]",
     &        "Gen", "Evnt", "pid"
      END IF
 9777 FORMAT (A6,9A15,2A10,A6)

*     ! Limit dumping to
*     !   - Boundary Crossing Estimators, BCEs (ISCRNG .EQ. 1)
*     !   - First BCE (JSCRNG .EQ. 1)
*     !   - Neutrons (IJ .EQ. 8) - Look for "Particle Code" in Manual
      
      PID = PID + 1
      
      IF ( (ISCRNG .EQ. 5) .AND. 
     &     ( (JSCRNG .EQ. 1) .OR. (JSCRNG .EQ. 2) .OR.
     &       (JSCRNG .EQ. 3) .OR. (JSCRNG .EQ. 4) ) ) THEN
*     !&       (JSCRNG .EQ. 5) .OR. (JSCRNG .EQ. 6) ) ) THEN
         
         IF (LAST_TPROD /= ATRACK) THEN
             EVENT_COUNT = EVENT_COUNT + 1
             LAST_TPROD = ATRACK
         END IF

         SELECT CASE (IJ)
         CASE (1)  ! proton
            MASS = 0.93827D0
         CASE (13, 14)  ! pi+ , pi-
            MASS = 0.13957D0
         CASE (10, 11)  ! mu+ , mu-
            MASS = 0.10566D0
         CASE (23)  ! pi0
            MASS = 0.13498D0
         CASE DEFAULT
            MASS = 0.0D0
         END SELECT

         EKIN = SQRT(PLA*PLA + MASS*MASS) - MASS
         
         WRITE(99, 7777)
     &        IJ, EKIN, PLA, XX, YY, ZZ, TXX, TYY, TZZ,
     &        ATRACK, LLO, EVENT_COUNT, PID
      
      END IF
 7777 FORMAT (I6,9E15.7,2I10,I6)


      IF (ISCRNG .EQ. 1) THEN

         IF ( (IJ .EQ. 13) .OR. (IJ .EQ. 14) .OR. (IJ .EQ. 10) .OR. (IJ .EQ. 11) ) THEN

         SELECT CASE (IJ)
         CASE (1)  ! proton
            MASS = 0.93827D0
         CASE (13, 14)  ! pi+ , pi-
            MASS = 0.13957D0
         CASE (10, 11)  ! mu+ , mu-
            MASS = 0.10566D0
         CASE (23)  ! pi0
            MASS = 0.13498D0
         CASE DEFAULT
            MASS = 0.0D0
         END SELECT

         MOM = SQRT(PLA*PLA - 2.0D0*PLA*MASS)

         IF (JSCRNG .EQ. 1) THEN
         WRITE(98, 9899)
     &        IJ, -PLA, MOM, XX, YY, ZZ, TXX, TYY, TZZ,
     &        ATRACK, LLO, EVENT_COUNT, PID
         END IF

         IF ( (JSCRNG .EQ. 2) .OR. (JSCRNG .EQ. 3) ) THEN
         WRITE(97, 9799)
     &        IJ, -PLA, MOM, XX, YY, ZZ, TXX, TYY, TZZ,
     &        ATRACK, LLO, EVENT_COUNT, PID
         END IF
         
         END IF
     
      END IF
 9899 FORMAT (I6,9E15.7,2I10,I6)
 9799 FORMAT (I6,9E15.7,2I10,I6)

      
************************************************************************
*
      RETURN
*=== End of function Fluscw ===========================================*
      END
