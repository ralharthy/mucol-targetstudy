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

      INTEGER TRACKID, PRODTYPE
      SAVE TRACKID
      DATA TRACKID /0/

*      COMMON /TRKCNT/ TRACKID
*      SAVE /TRKCNT/
*
*     ---- tag every particle, no condition ----

      IF ( NPSECN .EQ. 1 ) THEN
         ISPUSR(2) = ISPUSR(2) + 1
      ENDIF

      TRACKID   = TRACKID + 1
      ISPUSR(5) = ISPUSR(6)      ! parent's tracking ID (read before overwrite)
      ISPUSR(6) = TRACKID        ! this particle's own unique ID

      IF ( ISPUSR(8) .EQ. 0 ) THEN
         ISPUSR(8) = 1 ! The primary is a proton with IJ = 1
      END IF
      ISPUSR(1) = ISPUSR(8)
      ISPUSR(8) = IJ

*     ---- classify production mechanism ----
      IF ( LELEVT ) THEN
         PRODTYPE = 1
      ELSE IF ( LINEVT ) THEN
         PRODTYPE = 2
      ELSE IF ( LDECAY ) THEN
         PRODTYPE = 3         
      ELSE IF ( LDLTRY ) THEN
         PRODTYPE = 4
      ELSE IF ( LPAIRP ) THEN
         PRODTYPE = 5
      ELSE IF ( LBRMSP ) THEN
         PRODTYPE = 6
      ELSE IF ( LANNRS ) THEN
         PRODTYPE = 7
      ELSE IF ( LANNFL ) THEN
         PRODTYPE = 8
      ELSE IF ( LPHOEL ) THEN
         PRODTYPE = 9
      ELSE IF ( LCMPTN ) THEN
         PRODTYPE = 10
      ELSE IF ( LCOHSC ) THEN
         PRODTYPE = 11
      ELSE IF ( LLENSC ) THEN
         PRODTYPE = 12
      ELSE IF ( LOPPSC ) THEN
         PRODTYPE = 13
      ELSE IF ( LELDIS ) THEN
         PRODTYPE = 14
      ELSE IF ( LRDCAY ) THEN
         PRODTYPE = 15
      ELSE IF ( LSRPHO ) THEN
         PRODTYPE = 16
      ELSE
         PRODTYPE = 0
      ENDIF

      ISPUSR(3) = PRODTYPE
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