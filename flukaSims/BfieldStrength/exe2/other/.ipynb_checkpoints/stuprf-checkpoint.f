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

      INTEGER TRACKID
      SAVE TRACKID
      DATA TRACKID /0/

*      COMMON /TRKCNT/ TRACKID
*      SAVE /TRKCNT/
*
*     ---- tag every particle, no condition ----

      TRACKID   = (TRACKID + 1) !+ (ISPUSR(4) * 10000)
      ISPUSR(5) = ISPUSR(6)      ! parent's tracking ID (read before overwrite)
      ISPUSR(6) = TRACKID        ! this particle's own unique ID


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