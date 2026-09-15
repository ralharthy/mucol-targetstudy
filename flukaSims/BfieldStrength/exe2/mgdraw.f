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
      LOGICAL LFCOPE1, LFCOPE2, LFCOPE3
      LOGICAL LFCOPE4, LFCOPE5, LFCOPE6
      CHARACTER*8 NRGNAM, MRGNAM

      INTEGER PARENT_ID, NUCGEN, JTRKID, MTRKID, PRODTYP

      INTEGER TRACKID
      SAVE TRACKID
      DATA TRACKID /0/

      SAVE LFCOPE1, LFCOPE2, LFCOPE3
      SAVE LFCOPE4, LFCOPE5, LFCOPE6
      DATA LFCOPE1 / .FALSE. /
      DATA LFCOPE2 / .FALSE. /
      DATA LFCOPE3 / .FALSE. /
      DATA LFCOPE4 / .FALSE. /
      DATA LFCOPE5 / .FALSE. /
      DATA LFCOPE6 / .FALSE. /

      INTEGER IP
 
      IF ( .NOT. LFCOPE1 ) THEN
         LFCOPE1 = .TRUE.
         OPEN(UNIT=99, FILE='esc.txt', STATUS='UNKNOWN')
         WRITE(99,9999) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "Evnt", 
     &        "Mother", "ICODE"
      END IF
 9999 FORMAT (A6,9A15,4A7)

      IF ( .NOT. LFCOPE2 ) THEN
         LFCOPE2 = .TRUE.         
         OPEN(UNIT=98, FILE='prod.txt', STATUS='UNKNOWN')
         WRITE(98,9998) "# ID","E_kin[GeV]","P[GeV]",
     &        "x[cm]","y[cm]","z[cm]",
     &        "cx[-]","cy[-]","cz[-]", "T[s]", "Gen", "NEvnt",
     &        "Mother", "ICODE"
      ENDIF
 9998 FORMAT(A6,9A15,4A7)

      IF ( .NOT. LFCOPE3 ) THEN
         LFCOPE3 = .TRUE.
         OPEN(UNIT=97, FILE='det1.txt', STATUS='UNKNOWN')
         WRITE(97,9997) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "NEvnt", 
     &        "Mother", "ICODE"
      END IF
 9997 FORMAT (A6,9A15,4A7)

      IF ( .NOT. LFCOPE4 ) THEN
         LFCOPE4 = .TRUE.
         OPEN(UNIT=96, FILE='det2.txt', STATUS='UNKNOWN')
         WRITE(96,9996) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "NEvnt", 
     &        "Mother", "ICODE"
      END IF
 9996 FORMAT (A6,9A15,4A7)

      IF ( .NOT. LFCOPE5 ) THEN
         LFCOPE5 = .TRUE.
         OPEN(UNIT=95, FILE='det3.txt', STATUS='UNKNOWN')
         WRITE(95,9995) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "NEvnt", 
     &        "Mother", "ICODE"
      END IF
 9995 FORMAT (A6,9A15,4A7)

      IF ( .NOT. LFCOPE6 ) THEN
         LFCOPE6 = .TRUE.
         OPEN(UNIT=94, FILE='det4.txt', STATUS='UNKNOWN')
         WRITE(94,9994) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "NEvnt", 
     &        "Mother", "ICODE"
      END IF
 9994 FORMAT (A6,9A15,4A7)
 
      RETURN

      ! Boundary crossing: our interest
      ENTRY BXDRAW ( ICODE, MREG, NEWREG, XSCO, YSCO, ZSCO )
      CALL GEOR2N ( MREG,   MRGNAM, IERR1 )
      CALL GEOR2N ( NEWREG, NRGNAM, IERR2 )
      
      IF ( (JTRACK .NE. 1) .AND. (JTRACK .NE. 7) .AND. (JTRACK .NE. 8) .AND.
     &     (JTRACK .NE. 3) .AND. (JTRACK .NE. 4) .AND. (JTRACK .NE. 27) .AND.
     &     (JTRACK .NE. 28) .AND. (JTRACK .NE. 43) .AND. (JTRACK .NE. 44) .AND.
     &     (JTRACK .NE. 5) .AND. (JTRACK .NE. 6) .AND. (JTRACK .NE. 23) .AND.
     &     (JTRACK .GE. -6) ) THEN

      IF ( (NRGNAM .EQ. 'SOLENOID') .AND. (MRGNAM .EQ. 'TRG') ) THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(99, 9000) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, NUCGEN+1, NCASE, PARENT_ID, PRODTYP
      END IF

      IF ( (NRGNAM .EQ. 'BEAML1') .AND. (MRGNAM .EQ. 'SOLENOID') ) THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(97, 9777) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, NUCGEN+1, NCASE, PARENT_ID, PRODTYP
      END IF

      IF ( (NRGNAM .EQ. 'BEAML2') .AND. (MRGNAM .EQ. 'BEAML1') ) THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(96, 9666) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, NUCGEN+1, NCASE, PARENT_ID, PRODTYP
      END IF

      IF ( (NRGNAM .EQ. 'BEAML3') .AND. (MRGNAM .EQ. 'BEAML2') ) THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(95, 9555) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, NUCGEN+1, NCASE, PARENT_ID, PRODTYP
      END IF

      IF ( (NRGNAM .EQ. 'VOID') .AND. (MRGNAM .EQ. 'BEAML3') ) THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(94, 9444) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, NUCGEN+1, NCASE, PARENT_ID, PRODTYP
      END IF
      
      END IF
         
 9000 FORMAT (I6,9E15.7,4I7)
 9777 FORMAT (I6,9E15.7,4I7)
 9666 FORMAT (I6,9E15.7,4I7)
 9555 FORMAT (I6,9E15.7,4I7)
 9444 FORMAT (I6,9E15.7,4I7)
      RETURN

      ! Empty entries, not used
      ENTRY EEDRAW ( ICODE )
      RETURN

      ENTRY ENDRAW ( ICODE, MREG, RULL, XSCO, YSCO, ZSCO )
      RETURN
      
      ENTRY SODRAW
      RETURN

      ENTRY USDRAW ( ICODE, MREG, XSCO, YSCO, ZSCO )
      CALL GEOR2N ( MREG,   MRGNAM, IERR1 )

      ISPUSR(4) = NCASE

      TRACKID   = 0

      IF ( ((ICODE .EQ. 101) .OR. (ICODE .EQ. 102)) .AND. (MRGNAM .EQ. 'TRG') ) THEN

*           --- latching for genealogy, as before ---
            ISPUSR(1) = JTRACK
            ISPUSR(3) = ICODE
            ISPUSR(2) = ISPUSR(2) + 1 ! Generation

            ISPUSR(5) = ISPUSR(6)      ! parent's tracking ID (read before overwrite)
            

*           --- loop over ALL secondaries from this interaction
*               and write every one, unfiltered ---
            DO IP = 1, NP

            SPAUSR(3) = SPAUSR(3) + ATRACK   ! cumulative time, latched and
                                   ! propagated the same way as
                                   ! TrackID via the parent's
                                   ! stored SPAUSR before overwrite

            TRACKID   = (TRACKID + 1) !+ (ISPUSR(4) * 10000)
            ISPUSR(6) = TRACKID        ! this particle's own unique ID

            IF ( (KPART(IP) .NE. 1) .AND. (KPART(IP) .NE. 7) .AND. (KPART(IP) .NE. 8) .AND.
     &           (KPART(IP) .NE. 3) .AND. (KPART(IP) .NE. 4) .AND. (KPART(IP) .NE. 27) .AND.
     &           (KPART(IP) .NE. 28) .AND. (KPART(IP) .NE. 43) .AND. (KPART(IP) .NE. 44) ) THEN
               WRITE(98,9888)
     &              KPART(IP), TKI(IP), PLR(IP),
     &              XSCO, YSCO, ZSCO,
     &              CXR(IP), CYR(IP), CZR(IP), ATRACK, ISPUSR(2)+1, NCASE,
     &              JTRACK, ICODE

            PARENT_ID = ISPUSR(1)
            NUCGEN = ISPUSR(2)
            MTRKID = ISPUSR(5)
            JTRKID = ISPUSR(6)
            PRODTYP = ISPUSR(3)
      
            END IF

*  500       CONTINUE
            END DO
 9888       FORMAT(I6,9E15.7,4I7)

      ENDIF
      
      RETURN
      
*=== End of subrutine Mgdraw ==========================================*
      END
