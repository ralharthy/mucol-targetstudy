*                                                                      *
*=== mgdraw ===========================================================*
*                                                                      *
      SUBROUTINE MGDRAW ( ICODE, MREG )

      INCLUDE 'dblprc.inc'
      INCLUDE 'dimpar.inc'
      INCLUDE 'iounit.inc'
*
*----------------------------------------------------------------------*
*                                                                      *
*     Copyright (C) 2025:  CERN                                        *
*     All Rights Reserved.                                             *
*                                                                      *
*----------------------------------------------------------------------*
*
      INCLUDE 'caslim.inc'
      INCLUDE 'comput.inc'
      INCLUDE 'sourcm.inc'
      INCLUDE 'fheavy.inc'
      INCLUDE 'flkstk.inc'
      INCLUDE 'genstk.inc'
      INCLUDE 'mgddcm.inc'
      INCLUDE 'paprop.inc'
      INCLUDE 'quemgd.inc'
      INCLUDE 'sumcou.inc'
      INCLUDE 'trackr.inc'
      INCLUDE 'flkmat.inc'
*
*
      LOGICAL LFCOPE1, LFCOPE2
      CHARACTER*8 NRGNAM, MRGNAM

      INTEGER PARENT_ID, NUCGEN, JTRKID, MTRKID, PRODTYP

      INTEGER TRACKID
      SAVE TRACKID
      DATA TRACKID /0/

      SAVE LFCOPE1, LFCOPE2
      DATA LFCOPE1 / .FALSE. /
      DATA LFCOPE2 / .FALSE. /

      PARENT_ID = ISPUSR(1)
      NUCGEN = ISPUSR(2)
      MTRKID = ISPUSR(5)
      JTRKID = ISPUSR(6)
      PRODTYP = ISPUSR(3)
 
*      IF ( .NOT. LFCOPE1 ) THEN
*         LFCOPE1 = .TRUE.
*         OPEN(UNIT=98, FILE='esc.txt', STATUS='UNKNOWN')
*         WRITE(98,9898) "# ID", "E_kin[GeV]", "P[GeV/c]",
*     &        "x[cm]", "y[cm]", "z[cm]",
*     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "Evnt", "Mother",
*     &        "TrkId", "MId", "PrdTyp"
*      END IF
* 9898 FORMAT (A6,9A15,6A7)

      IF ( .NOT. LFCOPE2 ) THEN
         LFCOPE2 = .TRUE.
         OPEN(UNIT=97, FILE='det1.txt', STATUS='UNKNOWN')
         WRITE(97,9797) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "Evnt", "Mother",
     &        "TrkId", "MId", "PrdTyp"
      END IF
 9797 FORMAT (A6,9A15,6A7)
 
      RETURN

      ! Boundary crossing: our interest
      ENTRY BXDRAW ( ICODE, MREG, NEWREG, XSCO, YSCO, ZSCO )
      CALL GEOR2N ( MREG,   MRGNAM, IERR1 )
      CALL GEOR2N ( NEWREG, NRGNAM, IERR2 )
      
      IF ((JTRACK .EQ. 10) .OR. (JTRACK .EQ. 11) .OR. (JTRACK .EQ. 13) .OR. (JTRACK .EQ. 14)) THEN

*      IF (NRGNAM .EQ. 'BFIELD') THEN
*         EKIN = ETRACK-AM(JTRACK)
*         WRITE(98, 9888) JTRACK, ETRACK-AM(JTRACK), PTRACK,
*     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
*     &        ATRACK, LTRACK, NCASE, PARENT_ID, JTRKID, MTRKID, PRODTYP
*      END IF

      IF (NRGNAM .EQ. 'DET1') THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(97, 9777) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, LTRACK, NCASE, PARENT_ID, JTRKID, MTRKID, PRODTYP
      END IF
      
      END IF
         
* 9888 FORMAT (I6,9E15.7,6I7)
 9777 FORMAT (I6,9E15.7,6I7)
      RETURN

      ! Empty entries, not used
      ENTRY EEDRAW ( ICODE )
      RETURN

      ENTRY ENDRAW ( ICODE, MREG, RULL, XSCO, YSCO, ZSCO )
      RETURN
      
      ENTRY SODRAW

*     --- explicitly zero out tracking fields for every primary,
*         so that MoId correctly reads 0 for first-generation
*         secondaries produced directly from a primary ---

      DO 400 I = 1, NPFLKA

         ISPARK(1,I) = 0
         ISPARK(3,I) = 0
         ISPARK(5,I) = 0
         ISPARK(6,I) = 0

  400 CONTINUE

      RETURN
      
      RETURN

      ENTRY USDRAW ( ICODE, MREG, XSCO, YSCO, ZSCO )
*
*     JTRACK is the particle type of the particle CAUSING the interaction
*     i.e. the parent of whatever secondaries get produced here
*
      ISPUSR(4) = NCASE

*     --- parent info: JTRACK/TRACKR still reflect the CAUSING
*         particle at this point, and its own ISPUSR values (set
*         when IT was tagged as a secondary) are still sitting in
*         ISPUSR from before this call overwrites them ---

      IF ( (ICODE .EQ. 101) .OR. (ICODE .EQ. 102) ) THEN
         ISPUSR(1) = JTRACK
*         ISPUSR(5) = ISPUSR(6)     ! parent's tracking ID
*         TRACKID   = TRACKID + 1
*         ISPUSR(6) = TRACKID       ! this secondary's new unique ID
         
         ISPUSR(3) = ICODE         ! interaction/production mechanism,
                                   ! straight from FLUKA's own code
                                   ! rather than re-deriving via
                                   ! evtflg.inc logicals

         ISPUSR(2) = ISPUSR(2) + 1  ! interaction/generation count:
                                    ! parent's count, incremented by
                                    ! one for this new interaction
      ENDIF


*      ISPUSR(1) = JTRACK           ! parent's species code
*      ISPUSR(5) = ISPUSR(6)        ! parent's tracking ID (captured
*                                   ! BEFORE we overwrite ISPUSR(6)
*                                   ! below with this secondary's own)

*     --- this secondary s own info ---
*      TRACKID   = TRACKID + 1
*      ISPUSR(6) = TRACKID
*      ISPUSR(3) = ICODE            ! interaction/production mechanism,
*                                   ! straight from FLUKA's own code
*                                   ! rather than re-deriving via
*                                   ! evtflg.inc logicals

*      SPAUSR(1) = ETRACK - AM(JTRACK)
*      SPAUSR(2) = PTRACK
      
      RETURN
      
*=== End of subrutine Mgdraw ==========================================*
      END
