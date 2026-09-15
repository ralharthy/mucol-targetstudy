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

      SAVE LFCOPE1, LFCOPE2
      DATA LFCOPE1 / .FALSE. /
      DATA LFCOPE2 / .FALSE. /
 
      IF ( .NOT. LFCOPE1 ) THEN
         LFCOPE1 = .TRUE.
         OPEN(UNIT=98, FILE='trg.txt', STATUS='UNKNOWN')
         WRITE(98,9898) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "Evnt"
      END IF
 9898 FORMAT (A6,9A15,2A10)

      IF ( .NOT. LFCOPE2 ) THEN
         LFCOPE2 = .TRUE.
         OPEN(UNIT=97, FILE='det1.txt', STATUS='UNKNOWN')
         WRITE(97,9797) "# ID", "E_kin[GeV]", "P[GeV/c]",
     &        "x[cm]", "y[cm]", "z[cm]",
     &        "cx[-]", "cy[-]", "cz[-]", "T[s]", "Gen", "Evnt"
      END IF
 9797 FORMAT (A6,9A15,2A10)
 
      RETURN

      ! Boundary crossing: our interest
      ENTRY BXDRAW ( ICODE, MREG, NEWREG, XSCO, YSCO, ZSCO )
      CALL GEOR2N ( MREG,   MRGNAM, IERR1 )
      CALL GEOR2N ( NEWREG, NRGNAM, IERR2 )
      
      IF ((JTRACK .EQ. 10) .OR. (JTRACK .EQ. 11) .OR. (JTRACK .EQ. 13) .OR. (JTRACK .EQ. 14)) THEN

      IF (NRGNAM .EQ. 'BFIELD') THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(98, 9888) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, LTRACK, NCASE
      END IF

      IF (NRGNAM .EQ. 'DET1') THEN
         EKIN = ETRACK-AM(JTRACK)
         WRITE(97, 9777) JTRACK, ETRACK-AM(JTRACK), PTRACK,
     &        XSCO, YSCO, ZSCO, CXTRCK, CYTRCK, CZTRCK,
     &        ATRACK, LTRACK, NCASE
      END IF
      
      END IF
         
 9888 FORMAT (I6,9E15.7,2I10)
 9777 FORMAT (I6,9E15.7,2I10)
      RETURN

      ! Empty entries, not used
      ENTRY EEDRAW ( ICODE )
      RETURN

      ENTRY ENDRAW ( ICODE, MREG, RULL, XSCO, YSCO, ZSCO )
      RETURN
      
      ENTRY SODRAW
      RETURN
      
      ENTRY USDRAW ( ICODE, MREG, XSCO, YSCO, ZSCO )      
      RETURN
*=== End of subrutine Mgdraw ==========================================*
      END
