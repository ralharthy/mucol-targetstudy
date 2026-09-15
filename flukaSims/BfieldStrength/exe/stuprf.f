      SUBROUTINE STUPRF ( IJ, MREG, XX, YY, ZZ, NPSECN, NPPRMR )
      
      INCLUDE 'dblprc.inc'
      INCLUDE 'dimpar.inc'
      INCLUDE 'iounit.inc'
      INCLUDE 'evtflg.inc'
      INCLUDE 'flkstk.inc'
      INCLUDE 'fheavy.inc'
      INCLUDE 'genstk.inc'
      INCLUDE 'trackr.inc'
      INCLUDE 'caslim.inc'      ! for NCASE, if not already pulled in elsewhere
      INCLUDE 'paprop.inc'      ! <-- needed for AM(:)

*
*     ---- your tagging logic goes HERE, before the default copy loop ----
      IF ( LINEVT .OR. LDECAY ) THEN

         IF ( NPSECN .EQ. 1 ) THEN
            ISPUSR(3) = ISPUSR(3) + 1
         ENDIF
         ISPUSR(1) = IJ
         ISPUSR(2) = NCASE*1000 + NPFLKA
         ISPUSR(4) = LTRACK

         SPAUSR(1) = ETRACK-AM(IJ)
         SPAUSR(2) = PTRACK
         
      ENDIF

*     ---------------------------------------------------------------------
*
      DO 100 ISPR = 1, MKBMX1
         SPAREK (ISPR,NPFLKA) = SPAUSR (ISPR)
  100 CONTINUE
      DO 200 ISPR = 1, MKBMX2
         ISPARK (ISPR,NPFLKA) = ISPUSR (ISPR)
  200 CONTINUE
      RETURN
      
      END