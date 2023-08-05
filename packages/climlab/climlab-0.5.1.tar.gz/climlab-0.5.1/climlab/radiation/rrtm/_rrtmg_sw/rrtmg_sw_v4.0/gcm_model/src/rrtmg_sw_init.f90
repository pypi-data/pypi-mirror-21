!     path:      $Source$
!     author:    $Author: miacono $
!     revision:  $Revision: 30822 $
!     created:   $Date: 2016-12-29 15:53:24 -0500 (Thu, 29 Dec 2016) $

      module rrtmg_sw_init

!----------------------------------------------------------------------------
! Copyright (c) 2002-2016, Atmospheric & Environmental Research, Inc. (AER)
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!  * Redistributions of source code must retain the above copyright
!    notice, this list of conditions and the following disclaimer.
!  * Redistributions in binary form must reproduce the above copyright
!    notice, this list of conditions and the following disclaimer in the
!    documentation and/or other materials provided with the distribution.
!  * Neither the name of Atmospheric & Environmental Research, Inc., nor
!    the names of its contributors may be used to endorse or promote products
!    derived from this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
! ARE DISCLAIMED. IN NO EVENT SHALL ATMOSPHERIC & ENVIRONMENTAL RESEARCH, INC.,
! BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
! CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
! SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
! INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
! CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
! ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
! THE POSSIBILITY OF SUCH DAMAGE.
!                        (http://www.rtweb.aer.com/)
!----------------------------------------------------------------------------

! ------- Modules -------
      use parkind, only : im => kind_im, rb => kind_rb
      use rrsw_wvn
      use rrtmg_sw_setcoef, only: swatmref

      implicit none

      contains

! **************************************************************************
      subroutine rrtmg_sw_ini(cpdair)
! **************************************************************************
!
!  Original version:   Michael J. Iacono; February, 2004
!  Revision for F90 formatting:  M. J. Iacono, July, 2006
!
!  This subroutine performs calculations necessary for the initialization
!  of the shortwave model.  Lookup tables are computed for use in the SW
!  radiative transfer, and input absorption coefficient data for each
!  spectral band are reduced from 224 g-point intervals to 112.
! **************************************************************************

      use parrrsw, only : mg, nbndsw, ngptsw
      use rrsw_tbl, only: ntbl, tblint, pade, bpade, tau_tbl, exp_tbl
      use rrsw_vsn, only: hvrini, hnamini

      real(kind=rb), intent(in) :: cpdair     ! Specific heat capacity of dry air
                                              ! at constant pressure at 273 K
                                              ! (J kg-1 K-1)

! ------- Local -------

      integer(kind=im) :: ibnd, igc, ig, ind, ipr
      integer(kind=im) :: igcsm, iprsm
      integer(kind=im) :: itr

      real(kind=rb) :: wtsum, wtsm(mg)
      real(kind=rb) :: tfn

      real(kind=rb), parameter :: expeps = 1.e-20_rb   ! Smallest value for exponential table

! ------- Definitions -------
!     Arrays for 10000-point look-up tables:
!     TAU_TBL  Clear-sky optical depth
!     EXP_TBL  Exponential lookup table for transmittance
!     PADE     Pade approximation constant (= 0.278)
!     BPADE    Inverse of the Pade approximation constant
!

      hvrini = '$Revision: 30822 $'

! Initialize model data
      call swdatinit(cpdair)
      call swcmbdat              ! g-point interval reduction data
      call swaerpr               ! aerosol optical properties
      call swcldpr               ! cloud optical properties
      call swatmref              ! reference MLS profile
      call sw_kgb16              ! molecular absorption coefficients
      call sw_kgb17
      call sw_kgb18
      call sw_kgb19
      call sw_kgb20
      call sw_kgb21
      call sw_kgb22
      call sw_kgb23
      call sw_kgb24
      call sw_kgb25
      call sw_kgb26
      call sw_kgb27
      call sw_kgb28
      call sw_kgb29

! Define exponential lookup tables for transmittance. Tau is
! computed as a function of the tau transition function, and transmittance
! is calculated as a function of tau.  All tables are computed at intervals
! of 0.0001.  The inverse of the constant used in the Pade approximation to
! the tau transition function is set to bpade.

      exp_tbl(0) = 1.0_rb
      exp_tbl(ntbl) = expeps
      bpade = 1.0_rb / pade
      do itr = 1, ntbl-1
         tfn = real(itr,kind=rb) / real(ntbl,kind=rb)
         tau_tbl = bpade * tfn / (1._rb - tfn)
         exp_tbl(itr) = exp(-tau_tbl)
         if (exp_tbl(itr) .le. expeps) exp_tbl(itr) = expeps
      enddo

! Perform g-point reduction from 16 per band (224 total points) to
! a band dependent number (112 total points) for all absorption
! coefficient input data and Planck fraction input data.
! Compute relative weighting for new g-point combinations.

      igcsm = 0
      do ibnd = 1,nbndsw
         iprsm = 0
         if (ngc(ibnd).lt.mg) then
            do igc = 1,ngc(ibnd)
               igcsm = igcsm + 1
               wtsum = 0.
               do ipr = 1, ngn(igcsm)
                  iprsm = iprsm + 1
                  wtsum = wtsum + wt(iprsm)
               enddo
               wtsm(igc) = wtsum
            enddo
            do ig = 1, ng(ibnd+15)
               ind = (ibnd-1)*mg + ig
               rwgt(ind) = wt(ig)/wtsm(ngm(ind))
            enddo
         else
            do ig = 1, ng(ibnd+15)
               igcsm = igcsm + 1
               ind = (ibnd-1)*mg + ig
               rwgt(ind) = 1.0_rb
            enddo
         endif
      enddo

! Reduce g-points for absorption coefficient data in each LW spectral band.

      call cmbgb16s
      call cmbgb17
      call cmbgb18
      call cmbgb19
      call cmbgb20
      call cmbgb21
      call cmbgb22
      call cmbgb23
      call cmbgb24
      call cmbgb25
      call cmbgb26
      call cmbgb27
      call cmbgb28
      call cmbgb29

      end subroutine rrtmg_sw_ini

!***************************************************************************
      subroutine swdatinit(cpdair)
!***************************************************************************

! --------- Modules ----------

      use rrsw_con, only: heatfac, grav, planck, boltz, &
                          clight, avogad, alosmt, gascon, radcn1, radcn2, &
                          sbcnst, secdy
      use rrsw_vsn

      save

      real(kind=rb), intent(in) :: cpdair     ! Specific heat capacity of dry air
                                              ! at constant pressure at 273 K
                                              ! (J kg-1 K-1)

! Shortwave spectral band limits (wavenumbers)
      wavenum1(:) = (/2600._rb, 3250._rb, 4000._rb, 4650._rb, 5150._rb, 6150._rb, 7700._rb, &
                      8050._rb,12850._rb,16000._rb,22650._rb,29000._rb,38000._rb,  820._rb/)
      wavenum2(:) = (/3250._rb, 4000._rb, 4650._rb, 5150._rb, 6150._rb, 7700._rb, 8050._rb, &
                     12850._rb,16000._rb,22650._rb,29000._rb,38000._rb,50000._rb, 2600._rb/)
      delwave(:) =  (/ 650._rb,  750._rb,  650._rb,  500._rb, 1000._rb, 1550._rb,  350._rb, &
                      4800._rb, 3150._rb, 6650._rb, 6350._rb, 9000._rb,12000._rb, 1780._rb/)

! Spectral band information
      ng(:) = (/16,16,16,16,16,16,16,16,16,16,16,16,16,16/)
      nspa(:) = (/9,9,9,9,1,9,9,1,9,1,0,1,9,1/)
      nspb(:) = (/1,5,1,1,1,5,1,0,1,0,0,1,5,1/)

! Fundamental physical constants from NIST 2002

      grav = 9.8066_rb                        ! Acceleration of gravity
                                              ! (m s-2)
      planck = 6.62606876e-27_rb              ! Planck constant
                                              ! (ergs s; g cm2 s-1)
      boltz = 1.3806503e-16_rb                ! Boltzmann constant
                                              ! (ergs K-1; g cm2 s-2 K-1)
      clight = 2.99792458e+10_rb              ! Speed of light in a vacuum
                                              ! (cm s-1)
      avogad = 6.02214199e+23_rb              ! Avogadro constant
                                              ! (mol-1)
      alosmt = 2.6867775e+19_rb               ! Loschmidt constant
                                              ! (cm-3)
      gascon = 8.31447200e+07_rb              ! Molar gas constant
                                              ! (ergs mol-1 K-1)
      radcn1 = 1.191042772e-12_rb             ! First radiation constant
                                              ! (W cm2 sr-1)
      radcn2 = 1.4387752_rb                   ! Second radiation constant
                                              ! (cm K)
      sbcnst = 5.670400e-04_rb                ! Stefan-Boltzmann constant
                                              ! (W cm-2 K-4)
      secdy = 8.6400e4_rb                     ! Number of seconds per day
                                              ! (s d-1)
!
!     units are generally cgs
!
!     The first and second radiation constants are taken from NIST.
!     They were previously obtained from the relations:
!          radcn1 = 2.*planck*clight*clight*1.e-07
!          radcn2 = planck*clight/boltz

!     Heatfac is the factor by which delta-flux / delta-pressure is
!     multiplied, with flux in W/m-2 and pressure in mbar, to get
!     the heating rate in units of degrees/day.  It is equal to:
!     Original value:
!           (g)x(#sec/day)x(1e-5)/(specific heat of air at const. p)
!           Here, cpdair (1.004) is in units of J g-1 K-1, and the
!           constant (1.e-5) converts mb to Pa and g-1 to kg-1.
!        =  (9.8066)(86400)(1e-5)/(1.004)
!      heatfac = 8.4391_rb
!
!     Modified value for consistency with CAM3:
!           (g)x(#sec/day)x(1e-5)/(specific heat of air at const. p)
!           Here, cpdair (1.00464) is in units of J g-1 K-1, and the
!           constant (1.e-5) converts mb to Pa and g-1 to kg-1.
!        =  (9.80616)(86400)(1e-5)/(1.00464)
!      heatfac = 8.43339130434_rb
!
!     Calculated value (from constants above and input cpdair)
!        (grav) x (#sec/day) / (specific heat of dry air at const. p x 1.e2)
!           Here, cpdair is in units of J kg-1 K-1, and the constant (1.e2)
!           converts mb to Pa when heatfac is multiplied by W m-2 mb-1.
      heatfac = grav * secdy / (cpdair * 1.e2_rb)

      end subroutine swdatinit

!***************************************************************************
      subroutine swcmbdat
!***************************************************************************

      save

! ------- Definitions -------
!     Arrays for the g-point reduction from 224 to 112 for the 16 LW bands:
!     This mapping from 224 to 112 points has been carefully selected to
!     minimize the effect on the resulting fluxes and cooling rates, and
!     caution should be used if the mapping is modified.  The full 224
!     g-point set can be restored with ngpt=224, ngc=16*16, ngn=224*1., etc.
!     ngpt    The total number of new g-points
!     ngc     The number of new g-points in each band
!     ngs     The cumulative sum of new g-points for each band
!     ngm     The index of each new g-point relative to the original
!             16 g-points for each band.
!     ngn     The number of original g-points that are combined to make
!             each new g-point in each band.
!     ngb     The band index for each new g-point.
!     wt      RRTM weights for 16 g-points.

! Use this set for 112 quadrature point (g-point) model
! ------- Data statements -------
      ngc(:) = (/ 6,12, 8, 8,10,10, 2,10, 8, 6, 6, 8, 6,12 /)
      ngs(:) = (/ 6,18,26,34,44,54,56,66,74,80,86,94,100,112 /)
      ngm(:) = (/ 1,1,2,2,3,3,4,4,5,5,5,5,6,6,6,6, &           ! band 16
                  1,2,3,4,5,6,6,7,8,8,9,10,10,11,12,12, &      ! band 17
                  1,2,3,4,5,5,6,6,7,7,7,7,8,8,8,8, &           ! band 18
                  1,2,3,4,5,5,6,6,7,7,7,7,8,8,8,8, &           ! band 19
                  1,2,3,4,5,6,7,8,9,9,10,10,10,10,10,10, &     ! band 20
                  1,2,3,4,5,6,7,8,9,9,10,10,10,10,10,10, &     ! band 21
                  1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2, &           ! band 22
                  1,1,2,2,3,4,5,6,7,8,9,9,10,10,10,10, &       ! band 23
                  1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8, &           ! band 24
                  1,2,3,3,4,4,5,5,5,5,6,6,6,6,6,6, &           ! band 25
                  1,2,3,3,4,4,5,5,5,5,6,6,6,6,6,6, &           ! band 26
                  1,2,3,4,5,6,7,7,7,7,8,8,8,8,8,8, &           ! band 27
                  1,2,3,3,4,4,5,5,5,5,6,6,6,6,6,6, &           ! band 28
                  1,2,3,4,5,5,6,6,7,7,8,8,9,10,11,12 /)        ! band 29
      ngn(:) = (/ 2,2,2,2,4,4, &                               ! band 16
                  1,1,1,1,1,2,1,2,1,2,1,2, &                   ! band 17
                  1,1,1,1,2,2,4,4, &                           ! band 18
                  1,1,1,1,2,2,4,4, &                           ! band 19
                  1,1,1,1,1,1,1,1,2,6, &                       ! band 20
                  1,1,1,1,1,1,1,1,2,6, &                       ! band 21
                  8,8, &                                       ! band 22
                  2,2,1,1,1,1,1,1,2,4, &                       ! band 23
                  2,2,2,2,2,2,2,2, &                           ! band 24
                  1,1,2,2,4,6, &                               ! band 25
                  1,1,2,2,4,6, &                               ! band 26
                  1,1,1,1,1,1,4,6, &                           ! band 27
                  1,1,2,2,4,6, &                               ! band 28
                  1,1,1,1,2,2,2,2,1,1,1,1 /)                   ! band 29
      ngb(:) = (/ 16,16,16,16,16,16, &                         ! band 16
                  17,17,17,17,17,17,17,17,17,17,17,17, &       ! band 17
                  18,18,18,18,18,18,18,18, &                   ! band 18
                  19,19,19,19,19,19,19,19, &                   ! band 19
                  20,20,20,20,20,20,20,20,20,20, &             ! band 20
                  21,21,21,21,21,21,21,21,21,21, &             ! band 21
                  22,22, &                                     ! band 22
                  23,23,23,23,23,23,23,23,23,23, &             ! band 23
                  24,24,24,24,24,24,24,24, &                   ! band 24
                  25,25,25,25,25,25, &                         ! band 25
                  26,26,26,26,26,26, &                         ! band 26
                  27,27,27,27,27,27,27,27, &                   ! band 27
                  28,28,28,28,28,28, &                         ! band 28
                  29,29,29,29,29,29,29,29,29,29,29,29 /)       ! band 29

! Use this set for full 224 quadrature point (g-point) model
! ------- Data statements -------
!      ngc(:) = (/ 16,16,16,16,16,16,16,16,16,16,16,16,16,16 /)
!      ngs(:) = (/ 16,32,48,64,80,96,112,128,144,160,176,192,208,224 /)
!      ngm(:) = (/ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 16
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 17
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 18
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 19
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 20
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 21
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 22
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 23
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 24
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 25
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 26
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 27
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, &    ! band 28
!                  1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 /)    ! band 29
!      ngn(:) = (/ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 16
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 17
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 18
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 19
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 20
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 21
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 22
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 23
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 24
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 25
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 26
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 27
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, &           ! band 28
!                  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 /)           ! band 29
!      ngb(:) = (/ 16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16, &   ! band 16
!                  17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17, &   ! band 17
!                  18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18, &   ! band 18
!                  19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19, &   ! band 19
!                  20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20, &   ! band 20
!                  21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21, &   ! band 21
!                  22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22, &   ! band 22
!                  23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23, &   ! band 23
!                  24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24, &   ! band 24
!                  25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25, &   ! band 25
!                  26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26, &   ! band 26
!                  27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27, &   ! band 27
!                  28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28, &   ! band 28
!                  29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29 /)   ! band 29


      wt(:) =  (/ 0.1527534276_rb, 0.1491729617_rb, 0.1420961469_rb, &
                  0.1316886544_rb, 0.1181945205_rb, 0.1019300893_rb, &
                  0.0832767040_rb, 0.0626720116_rb, 0.0424925000_rb, &
                  0.0046269894_rb, 0.0038279891_rb, 0.0030260086_rb, &
                  0.0022199750_rb, 0.0014140010_rb, 0.0005330000_rb, &
                  0.0000750000_rb /)

      end subroutine swcmbdat

!***************************************************************************
      subroutine swaerpr
!***************************************************************************

! Purpose: Define spectral aerosol properties for six ECMWF aerosol types
! as used in the ECMWF IFS model (see module rrsw_aer.F90 for details)
!
! Original: Defined for rrtmg_sw 14 spectral bands, JJMorcrette, ECMWF Feb 2003
! Revision: Reformatted for consistency with rrtmg_lw, MJIacono, AER, Jul 2006

      use rrsw_aer, only : rsrtaua, rsrpiza, rsrasya

      save

      rsrtaua( 1, :) = (/ &
        0.10849_rb, 0.66699_rb, 0.65255_rb, 0.11600_rb, 0.06529_rb, 0.04468_rb/)
      rsrtaua( 2, :) = (/ &
        0.10849_rb, 0.66699_rb, 0.65255_rb, 0.11600_rb, 0.06529_rb, 0.04468_rb/)
      rsrtaua( 3, :) = (/ &
        0.20543_rb, 0.84642_rb, 0.84958_rb, 0.21673_rb, 0.28270_rb, 0.10915_rb/)
      rsrtaua( 4, :) = (/ &
        0.20543_rb, 0.84642_rb, 0.84958_rb, 0.21673_rb, 0.28270_rb, 0.10915_rb/)
      rsrtaua( 5, :) = (/ &
        0.20543_rb, 0.84642_rb, 0.84958_rb, 0.21673_rb, 0.28270_rb, 0.10915_rb/)
      rsrtaua( 6, :) = (/ &
        0.20543_rb, 0.84642_rb, 0.84958_rb, 0.21673_rb, 0.28270_rb, 0.10915_rb/)
      rsrtaua( 7, :) = (/ &
        0.20543_rb, 0.84642_rb, 0.84958_rb, 0.21673_rb, 0.28270_rb, 0.10915_rb/)
      rsrtaua( 8, :) = (/ &
        0.52838_rb, 0.93285_rb, 0.93449_rb, 0.53078_rb, 0.67148_rb, 0.46608_rb/)
      rsrtaua( 9, :) = (/ &
        0.52838_rb, 0.93285_rb, 0.93449_rb, 0.53078_rb, 0.67148_rb, 0.46608_rb/)
      rsrtaua(10, :) = (/ &
        1.69446_rb, 1.11855_rb, 1.09212_rb, 1.72145_rb, 1.03858_rb, 1.12044_rb/)
      rsrtaua(11, :) = (/ &
        1.69446_rb, 1.11855_rb, 1.09212_rb, 1.72145_rb, 1.03858_rb, 1.12044_rb/)
      rsrtaua(12, :) = (/ &
        1.69446_rb, 1.11855_rb, 1.09212_rb, 1.72145_rb, 1.03858_rb, 1.12044_rb/)
      rsrtaua(13, :) = (/ &
        1.69446_rb, 1.11855_rb, 1.09212_rb, 1.72145_rb, 1.03858_rb, 1.12044_rb/)
      rsrtaua(14, :) = (/ &
        0.10849_rb, 0.66699_rb, 0.65255_rb, 0.11600_rb, 0.06529_rb, 0.04468_rb/)

      rsrpiza( 1, :) = (/ &
        .5230504_rb, .7868518_rb, .8531531_rb, .4048149_rb, .8748231_rb, .2355667_rb/)
      rsrpiza( 2, :) = (/ &
        .5230504_rb, .7868518_rb, .8531531_rb, .4048149_rb, .8748231_rb, .2355667_rb/)
      rsrpiza( 3, :) = (/ &
        .8287144_rb, .9949396_rb, .9279543_rb, .6765051_rb, .9467578_rb, .9955938_rb/)
      rsrpiza( 4, :) = (/ &
        .8287144_rb, .9949396_rb, .9279543_rb, .6765051_rb, .9467578_rb, .9955938_rb/)
      rsrpiza( 5, :) = (/ &
        .8287144_rb, .9949396_rb, .9279543_rb, .6765051_rb, .9467578_rb, .9955938_rb/)
      rsrpiza( 6, :) = (/ &
        .8287144_rb, .9949396_rb, .9279543_rb, .6765051_rb, .9467578_rb, .9955938_rb/)
      rsrpiza( 7, :) = (/ &
        .8287144_rb, .9949396_rb, .9279543_rb, .6765051_rb, .9467578_rb, .9955938_rb/)
      rsrpiza( 8, :) = (/ &
        .8970131_rb, .9984940_rb, .9245594_rb, .7768385_rb, .9532763_rb, .9999999_rb/)
      rsrpiza( 9, :) = (/ &
        .8970131_rb, .9984940_rb, .9245594_rb, .7768385_rb, .9532763_rb, .9999999_rb/)
      rsrpiza(10, :) = (/ &
        .9148907_rb, .9956173_rb, .7504584_rb, .8131335_rb, .9401905_rb, .9999999_rb/)
      rsrpiza(11, :) = (/ &
        .9148907_rb, .9956173_rb, .7504584_rb, .8131335_rb, .9401905_rb, .9999999_rb/)
      rsrpiza(12, :) = (/ &
        .9148907_rb, .9956173_rb, .7504584_rb, .8131335_rb, .9401905_rb, .9999999_rb/)
      rsrpiza(13, :) = (/ &
        .9148907_rb, .9956173_rb, .7504584_rb, .8131335_rb, .9401905_rb, .9999999_rb/)
      rsrpiza(14, :) = (/ &
        .5230504_rb, .7868518_rb, .8531531_rb, .4048149_rb, .8748231_rb, .2355667_rb/)

      rsrasya( 1, :) = (/ &
        0.700610_rb, 0.818871_rb, 0.702399_rb, 0.689886_rb, .4629866_rb, .1907639_rb/)
      rsrasya( 2, :) = (/ &
        0.700610_rb, 0.818871_rb, 0.702399_rb, 0.689886_rb, .4629866_rb, .1907639_rb/)
      rsrasya( 3, :) = (/ &
        0.636342_rb, 0.802467_rb, 0.691305_rb, 0.627497_rb, .6105750_rb, .4760794_rb/)
      rsrasya( 4, :) = (/ &
        0.636342_rb, 0.802467_rb, 0.691305_rb, 0.627497_rb, .6105750_rb, .4760794_rb/)
      rsrasya( 5, :) = (/ &
        0.636342_rb, 0.802467_rb, 0.691305_rb, 0.627497_rb, .6105750_rb, .4760794_rb/)
      rsrasya( 6, :) = (/ &
        0.636342_rb, 0.802467_rb, 0.691305_rb, 0.627497_rb, .6105750_rb, .4760794_rb/)
      rsrasya( 7, :) = (/ &
        0.636342_rb, 0.802467_rb, 0.691305_rb, 0.627497_rb, .6105750_rb, .4760794_rb/)
      rsrasya( 8, :) = (/ &
        0.668431_rb, 0.788530_rb, 0.698682_rb, 0.657422_rb, .6735182_rb, .6519706_rb/)
      rsrasya( 9, :) = (/ &
        0.668431_rb, 0.788530_rb, 0.698682_rb, 0.657422_rb, .6735182_rb, .6519706_rb/)
      rsrasya(10, :) = (/ &
        0.729019_rb, 0.803129_rb, 0.784592_rb, 0.712208_rb, .7008249_rb, .7270548_rb/)
      rsrasya(11, :) = (/ &
        0.729019_rb, 0.803129_rb, 0.784592_rb, 0.712208_rb, .7008249_rb, .7270548_rb/)
      rsrasya(12, :) = (/ &
        0.729019_rb, 0.803129_rb, 0.784592_rb, 0.712208_rb, .7008249_rb, .7270548_rb/)
      rsrasya(13, :) = (/ &
        0.729019_rb, 0.803129_rb, 0.784592_rb, 0.712208_rb, .7008249_rb, .7270548_rb/)
      rsrasya(14, :) = (/ &
        0.700610_rb, 0.818871_rb, 0.702399_rb, 0.689886_rb, .4629866_rb, .1907639_rb/)

      end subroutine swaerpr

!***************************************************************************
      subroutine cmbgb16s
!***************************************************************************
!
!  Original version:       MJIacono; July 1998
!  Revision for RRTM_SW:   MJIacono; November 2002
!  Revision for RRTMG_SW:  MJIacono; December 2003
!  Revision for F90 reformatting:  MJIacono; July 2006
!
!  The subroutines CMBGB16->CMBGB29 input the absorption coefficient
!  data for each band, which are defined for 16 g-points and 14 spectral
!  bands. The data are combined with appropriate weighting following the
!  g-point mapping arrays specified in RRTMG_SW_INIT.  Solar source
!  Function data in array SFLUXREF are combined without weighting.  All
!  g-point reduced data are put into new arrays for use in RRTMG_SW.
!
!  band 16:  2600-3250 cm-1 (low key- h2o,ch4; high key - ch4)
!
!-----------------------------------------------------------------------

      use rrsw_kg16, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(1)
                  sumk = 0._rb
                  do ipr = 1, ngn(igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,5
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(1)
               sumk = 0._rb
               do ipr = 1, ngn(igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(1)
            sumk = 0._rb
            do ipr = 1, ngn(igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,3
         iprsm = 0
         do igc = 1,ngc(1)
            sumk = 0._rb
            do ipr = 1, ngn(igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(1)
         sumf = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(igc)
            iprsm = iprsm + 1
            sumf = sumf + sfluxrefo(iprsm)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         sfluxref(igc) = sumf
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb16s

!***************************************************************************
      subroutine cmbgb17
!***************************************************************************
!
!     band 17:  3250-4000 cm-1 (low - h2o,co2; high - h2o,co2)
!-----------------------------------------------------------------------

      use rrsw_kg17, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(2)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(1)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+16)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jn = 1,5
         do jt = 1,5
            do jp = 13,59
               iprsm = 0
               do igc = 1,ngc(2)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(1)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kbo(jn,jt,jp,iprsm)*rwgt(iprsm+16)
                  enddo
                  kb(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(2)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(1)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+16)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,4
         iprsm = 0
         do igc = 1,ngc(2)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(1)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+16)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      do jp = 1,5
         iprsm = 0
         do igc = 1,ngc(2)
            sumf = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(1)+igc)
               iprsm = iprsm + 1
               sumf = sumf + sfluxrefo(iprsm,jp)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb17

!***************************************************************************
      subroutine cmbgb18
!***************************************************************************
!
!     band 18:  4000-4650 cm-1 (low - h2o,ch4; high - ch4)
!-----------------------------------------------------------------------

      use rrsw_kg18, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(3)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(2)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+32)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,5
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(3)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(2)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+32)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(3)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(2)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+32)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,3
         iprsm = 0
         do igc = 1,ngc(3)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(2)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+32)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      do jp = 1,9
         iprsm = 0
         do igc = 1,ngc(3)
            sumf = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(2)+igc)
               iprsm = iprsm + 1
               sumf = sumf + sfluxrefo(iprsm,jp)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb18

!***************************************************************************
      subroutine cmbgb19
!***************************************************************************
!
!     band 19:  4650-5150 cm-1 (low - h2o,co2; high - co2)
!-----------------------------------------------------------------------

      use rrsw_kg19, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(4)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(3)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+48)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,5
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(4)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(3)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+48)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(4)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(3)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+48)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,3
         iprsm = 0
         do igc = 1,ngc(4)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(3)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+48)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      do jp = 1,9
         iprsm = 0
         do igc = 1,ngc(4)
            sumf = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(3)+igc)
               iprsm = iprsm + 1
               sumf = sumf + sfluxrefo(iprsm,jp)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb19

!***************************************************************************
      subroutine cmbgb20
!***************************************************************************
!
!     band 20:  5150-6150 cm-1 (low - h2o; high - h2o)
!-----------------------------------------------------------------------

      use rrsw_kg20, only : kao, kbo, selfrefo, forrefo, sfluxrefo, absch4o, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, absch4, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf1, sumf2, sumsv1, sumsv2, sumsv3


      do jt = 1,5
         do jp = 1,13
            iprsm = 0
            do igc = 1,ngc(5)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(4)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kao(jt,jp,iprsm)*rwgt(iprsm+64)
               enddo
               ka(jt,jp,igc) = sumk
            enddo
         enddo
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(5)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(4)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+64)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(5)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(4)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+64)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,4
         iprsm = 0
         do igc = 1,ngc(5)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(4)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+64)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(5)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(ngs(4)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + sfluxrefo(iprsm)
            sumf2 = sumf2 + absch4o(iprsm)*rwgt(iprsm+64)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         sfluxref(igc) = sumf1
         absch4(igc) = sumf2
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb20

!***************************************************************************
      subroutine cmbgb21
!***************************************************************************
!
!     band 21:  6150-7700 cm-1 (low - h2o,co2; high - h2o,co2)
!-----------------------------------------------------------------------

      use rrsw_kg21, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(6)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(5)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+80)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jn = 1,5
         do jt = 1,5
            do jp = 13,59
               iprsm = 0
               do igc = 1,ngc(6)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(5)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kbo(jn,jt,jp,iprsm)*rwgt(iprsm+80)
                  enddo
                  kb(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(6)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(5)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+80)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,4
         iprsm = 0
         do igc = 1,ngc(6)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(5)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+80)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      do jp = 1,9
         iprsm = 0
         do igc = 1,ngc(6)
            sumf = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(5)+igc)
               iprsm = iprsm + 1
               sumf = sumf + sfluxrefo(iprsm,jp)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb21

!***************************************************************************
      subroutine cmbgb22
!***************************************************************************
!
!     band 22:  7700-8050 cm-1 (low - h2o,o2; high - o2)
!-----------------------------------------------------------------------

      use rrsw_kg22, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(7)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(6)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+96)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,5
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(7)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(6)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+96)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(7)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(6)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+96)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,3
         iprsm = 0
         do igc = 1,ngc(7)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(6)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+96)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      do jp = 1,9
         iprsm = 0
         do igc = 1,ngc(7)
            sumf = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(6)+igc)
               iprsm = iprsm + 1
               sumf = sumf + sfluxrefo(iprsm,jp)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb22

!***************************************************************************
      subroutine cmbgb23
!***************************************************************************
!
!     band 23:  8050-12850 cm-1 (low - h2o; high - nothing)
!-----------------------------------------------------------------------

      use rrsw_kg23, only : kao, selfrefo, forrefo, sfluxrefo, raylo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, selfref, forref, sfluxref, rayl, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf1, sumf2, sumsv1, sumsv2, sumsv3


      do jt = 1,5
         do jp = 1,13
            iprsm = 0
            do igc = 1,ngc(8)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(7)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kao(jt,jp,iprsm)*rwgt(iprsm+112)
               enddo
               ka(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(8)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(7)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+112)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,3
         iprsm = 0
         do igc = 1,ngc(8)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(7)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+112)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(8)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(ngs(7)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + sfluxrefo(iprsm)
            sumf2 = sumf2 + raylo(iprsm)*rwgt(iprsm+112)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         sfluxref(igc) = sumf1
         rayl(igc) = sumf2
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb23

!***************************************************************************
      subroutine cmbgb24
!***************************************************************************
!
!     band 24:  12850-16000 cm-1 (low - h2o,o2; high - o2)
!-----------------------------------------------------------------------

      use rrsw_kg24, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            abso3ao, abso3bo, raylao, raylbo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            abso3a, abso3b, rayla, raylb, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf1, sumf2, sumf3, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(9)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(8)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+128)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jt = 1,5
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(9)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(8)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+128)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(9)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(8)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+128)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,3
         iprsm = 0
         do igc = 1,ngc(9)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(8)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+128)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(9)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumf3 = 0._rb
         do ipr = 1, ngn(ngs(8)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + raylbo(iprsm)*rwgt(iprsm+128)
            sumf2 = sumf2 + abso3ao(iprsm)*rwgt(iprsm+128)
            sumf3 = sumf3 + abso3bo(iprsm)*rwgt(iprsm+128)
         enddo
         raylb(igc) = sumf1
         abso3a(igc) = sumf2
         abso3b(igc) = sumf3
      enddo

      do jp = 1,9
         iprsm = 0
         do igc = 1,ngc(9)
            sumf1 = 0._rb
            sumf2 = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(8)+igc)
               iprsm = iprsm + 1
               sumf1 = sumf1 + sfluxrefo(iprsm,jp)
               sumf2 = sumf2 + raylao(iprsm,jp)*rwgt(iprsm+128)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf1
            rayla(igc,jp) = sumf2
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb24

!***************************************************************************
      subroutine cmbgb25
!***************************************************************************
!
!     band 25:  16000-22650 cm-1 (low - h2o; high - nothing)
!-----------------------------------------------------------------------

      use rrsw_kg25, only : kao, sfluxrefo, &
                            abso3ao, abso3bo, raylo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, sfluxref, &
                            abso3a, abso3b, rayl, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf1, sumf2, sumf3, sumf4, sumsv1, sumsv2, sumsv3


      do jt = 1,5
         do jp = 1,13
            iprsm = 0
            do igc = 1,ngc(10)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(9)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kao(jt,jp,iprsm)*rwgt(iprsm+144)
               enddo
               ka(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(10)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumf3 = 0._rb
         sumf4 = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(ngs(9)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + sfluxrefo(iprsm)
            sumf2 = sumf2 + abso3ao(iprsm)*rwgt(iprsm+144)
            sumf3 = sumf3 + abso3bo(iprsm)*rwgt(iprsm+144)
            sumf4 = sumf4 + raylo(iprsm)*rwgt(iprsm+144)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         sfluxref(igc) = sumf1
         abso3a(igc) = sumf2
         abso3b(igc) = sumf3
         rayl(igc) = sumf4
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb25

!***************************************************************************
      subroutine cmbgb26
!***************************************************************************
!
!     band 26:  22650-29000 cm-1 (low - nothing; high - nothing)
!-----------------------------------------------------------------------

      use rrsw_kg26, only : sfluxrefo, raylo, &
                            irradnceo, facbrghto, snsptdrko, &
                            sfluxref, rayl, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: igc, ipr, iprsm
      real(kind=rb) :: sumf1, sumf2, sumsv1, sumsv2, sumsv3


      iprsm = 0
      do igc = 1,ngc(11)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(ngs(10)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + raylo(iprsm)*rwgt(iprsm+160)
            sumf2 = sumf2 + sfluxrefo(iprsm)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         rayl(igc) = sumf1
         sfluxref(igc) = sumf2
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb26

!***************************************************************************
      subroutine cmbgb27
!***************************************************************************
!
!     band 27:  29000-38000 cm-1 (low - o3; high - o3)
!-----------------------------------------------------------------------

      use rrsw_kg27, only : kao, kbo, sfluxrefo, raylo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, sfluxref, rayl, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf1, sumf2, sumsv1, sumsv2, sumsv3


      do jt = 1,5
         do jp = 1,13
            iprsm = 0
            do igc = 1,ngc(12)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(11)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kao(jt,jp,iprsm)*rwgt(iprsm+176)
               enddo
               ka(jt,jp,igc) = sumk
            enddo
         enddo
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(12)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(11)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+176)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(12)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(ngs(11)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + sfluxrefo(iprsm)
            sumf2 = sumf2 + raylo(iprsm)*rwgt(iprsm+176)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         sfluxref(igc) = sumf1
         rayl(igc) = sumf2
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb27

!***************************************************************************
      subroutine cmbgb28
!***************************************************************************
!
!     band 28:  38000-50000 cm-1 (low - o3,o2; high - o3,o2)
!-----------------------------------------------------------------------

      use rrsw_kg28, only : kao, kbo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absa, ka, absb, kb, sfluxref, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jn, jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf, sumsv1, sumsv2, sumsv3


      do jn = 1,9
         do jt = 1,5
            do jp = 1,13
               iprsm = 0
               do igc = 1,ngc(13)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(12)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kao(jn,jt,jp,iprsm)*rwgt(iprsm+192)
                  enddo
                  ka(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jn = 1,5
         do jt = 1,5
            do jp = 13,59
               iprsm = 0
               do igc = 1,ngc(13)
                  sumk = 0._rb
                  do ipr = 1, ngn(ngs(12)+igc)
                     iprsm = iprsm + 1
                     sumk = sumk + kbo(jn,jt,jp,iprsm)*rwgt(iprsm+192)
                  enddo
                  kb(jn,jt,jp,igc) = sumk
               enddo
            enddo
         enddo
      enddo

      do jp = 1,5
         iprsm = 0
         do igc = 1,ngc(13)
            sumf = 0._rb
            sumsv1 = 0._rb
            sumsv2 = 0._rb
            sumsv3 = 0._rb
            do ipr = 1, ngn(ngs(12)+igc)
               iprsm = iprsm + 1
               sumf = sumf + sfluxrefo(iprsm,jp)
               sumsv1 = sumsv1 + irradnceo(iprsm,jp)
               sumsv2 = sumsv2 + facbrghto(iprsm,jp)
               sumsv3 = sumsv3 + snsptdrko(iprsm,jp)
            enddo
            sfluxref(igc,jp) = sumf
            irradnce(igc,jp) = sumsv1
            facbrght(igc,jp) = sumsv2
            snsptdrk(igc,jp) = sumsv3
         enddo
      enddo

      end subroutine cmbgb28

!***************************************************************************
      subroutine cmbgb29
!***************************************************************************
!
!     band 29:  820-2600 cm-1 (low - h2o; high - co2)
!-----------------------------------------------------------------------

      use rrsw_kg29, only : kao, kbo, selfrefo, forrefo, sfluxrefo, &
                            irradnceo, facbrghto, snsptdrko, &
                            absh2oo, absco2o, &
                            absa, ka, absb, kb, selfref, forref, sfluxref, &
                            absh2o, absco2, &
                            irradnce, facbrght, snsptdrk

! ------- Local -------
      integer(kind=im) :: jt, jp, igc, ipr, iprsm
      real(kind=rb) :: sumk, sumf1, sumf2, sumf3, sumsv1, sumsv2, sumsv3


      do jt = 1,5
         do jp = 1,13
            iprsm = 0
            do igc = 1,ngc(14)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(13)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kao(jt,jp,iprsm)*rwgt(iprsm+208)
               enddo
               ka(jt,jp,igc) = sumk
            enddo
         enddo
         do jp = 13,59
            iprsm = 0
            do igc = 1,ngc(14)
               sumk = 0._rb
               do ipr = 1, ngn(ngs(13)+igc)
                  iprsm = iprsm + 1
                  sumk = sumk + kbo(jt,jp,iprsm)*rwgt(iprsm+208)
               enddo
               kb(jt,jp,igc) = sumk
            enddo
         enddo
      enddo

      do jt = 1,10
         iprsm = 0
         do igc = 1,ngc(14)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(13)+igc)
               iprsm = iprsm + 1
               sumk = sumk + selfrefo(jt,iprsm)*rwgt(iprsm+208)
            enddo
            selfref(jt,igc) = sumk
         enddo
      enddo

      do jt = 1,4
         iprsm = 0
         do igc = 1,ngc(14)
            sumk = 0._rb
            do ipr = 1, ngn(ngs(13)+igc)
               iprsm = iprsm + 1
               sumk = sumk + forrefo(jt,iprsm)*rwgt(iprsm+208)
            enddo
            forref(jt,igc) = sumk
         enddo
      enddo

      iprsm = 0
      do igc = 1,ngc(14)
         sumf1 = 0._rb
         sumf2 = 0._rb
         sumf3 = 0._rb
         sumsv1 = 0._rb
         sumsv2 = 0._rb
         sumsv3 = 0._rb
         do ipr = 1, ngn(ngs(13)+igc)
            iprsm = iprsm + 1
            sumf1 = sumf1 + sfluxrefo(iprsm)
            sumf2 = sumf2 + absco2o(iprsm)*rwgt(iprsm+208)
            sumf3 = sumf3 + absh2oo(iprsm)*rwgt(iprsm+208)
            sumsv1 = sumsv1 + irradnceo(iprsm)
            sumsv2 = sumsv2 + facbrghto(iprsm)
            sumsv3 = sumsv3 + snsptdrko(iprsm)
         enddo
         sfluxref(igc) = sumf1
         absco2(igc) = sumf2
         absh2o(igc) = sumf3
         irradnce(igc) = sumsv1
         facbrght(igc) = sumsv2
         snsptdrk(igc) = sumsv3
      enddo

      end subroutine cmbgb29

!***********************************************************************
      subroutine swcldpr
!***********************************************************************

! Purpose: Define cloud extinction coefficient, single scattering albedo
!          and asymmetry parameter data.
!

! ------- Modules -------

      use rrsw_cld, only : extliq1, ssaliq1, asyliq1, &
                           extice2, ssaice2, asyice2, &
                           extice3, ssaice3, asyice3, fdlice3, &
                           abari, bbari, cbari, dbari, ebari, fbari

      save

!-----------------------------------------------------------------------
!
! Explanation of the method for each value of INFLAG.  A value of
!  0 for INFLAG do not distingish being liquid and ice clouds.
!  INFLAG = 2 does distinguish between liquid and ice clouds, and
!    requires further user input to specify the method to be used to
!    compute the aborption due to each.
!  INFLAG = 0:  For each cloudy layer, the cloud fraction, the cloud optical
!    depth, the cloud single-scattering albedo, and the
!    moments of the phase function (0:NSTREAM).  Note
!    that these values are delta-m scaled within this
!    subroutine.

!  INFLAG = 2:  For each cloudy layer, the cloud fraction, cloud
!    water path (g/m2), and cloud ice fraction are input.
!  ICEFLAG = 2:  The ice effective radius (microns) is input and the
!    optical properties due to ice clouds are computed from
!    the optical properties stored in the RT code, STREAMER v3.0
!    (Reference: Key. J., Streamer User's Guide, Cooperative
!    Institute for Meteorological Satellite Studies, 2001, 96 pp.).
!    Valid range of values for re are between 5.0 and
!    131.0 micron.
!    This version uses Ebert and Curry, JGR, (1992) method for
!    ice particles larger than 131.0 microns.
!  ICEFLAG = 3:  The ice generalized effective size (dge) is input
!    and the optical depths, single-scattering albedo,
!    and phase function moments are calculated as in
!    Q. Fu, J. Climate, (1996). Q. Fu provided high resolution
!    tables which were appropriately averaged for the
!    bands in RRTM_SW.  Linear interpolation is used to
!    get the coefficients from the stored tables.
!    Valid range of values for dge are between 5.0 and
!    140.0 micron.
!    This version uses Ebert and Curry, JGR, (1992) method for
!    ice particles larger than 140.0 microns.
!  LIQFLAG = 1:  The water droplet effective radius (microns) is input
!    and the optical depths due to water clouds are computed
!    as in Hu and Stamnes, J., Clim., 6, 728-742, (1993) with
!    modified coefficients derived from Mie scattering calculations.
!    The values for absorption coefficients appropriate for
!    the spectral bands in RRTM/RRTMG have been obtained for a
!    range of effective radii by an averaging procedure
!    based on the work of J. Pinto (private communication).
!    Linear interpolation is used to get the absorption
!    coefficients for the input effective radius.
!
!     ------------------------------------------------------------------

! Everything below is for INFLAG = 2.

! Coefficients for Ebert and Curry method
      abari(:) = (/ &
        & 3.448e-03_rb,3.448e-03_rb,3.448e-03_rb,3.448e-03_rb,3.448e-03_rb /)
      bbari(:) = (/ &
        & 2.431e+00_rb,2.431e+00_rb,2.431e+00_rb,2.431e+00_rb,2.431e+00_rb /)
      cbari(:) = (/ &
        & 1.000e-05_rb,1.100e-04_rb,1.240e-02_rb,3.779e-02_rb,4.666e-01_rb /)
      dbari(:) = (/ &
        & 0.000e+00_rb,1.405e-05_rb,6.867e-04_rb,1.284e-03_rb,2.050e-05_rb /)
      ebari(:) = (/ &
        & 7.661e-01_rb,7.730e-01_rb,7.865e-01_rb,8.172e-01_rb,9.595e-01_rb /)
      fbari(:) = (/ &
        & 5.851e-04_rb,5.665e-04_rb,7.204e-04_rb,7.463e-04_rb,1.076e-04_rb /)

! LIQFLAG==1 extinction coefficients, single scattering albedos, and asymmetry parameters
!   Derived from on Mie scattering computations; based on Hu & Stamnes coefficients
!     BAND  16
      extliq1(:, 16) = (/ &
        & 9.004493E-01_rb,6.366723E-01_rb,4.542354E-01_rb,3.468253E-01_rb,2.816431E-01_rb,&
        & 2.383415E-01_rb,2.070854E-01_rb,1.831854E-01_rb,1.642115E-01_rb,1.487539E-01_rb,&
        & 1.359169E-01_rb,1.250900E-01_rb,1.158354E-01_rb,1.078400E-01_rb,1.008646E-01_rb,&
        & 9.472307E-02_rb,8.928000E-02_rb,8.442308E-02_rb,8.005924E-02_rb,7.612231E-02_rb,&
        & 7.255153E-02_rb,6.929539E-02_rb,6.631769E-02_rb,6.358153E-02_rb,6.106231E-02_rb,&
        & 5.873077E-02_rb,5.656924E-02_rb,5.455769E-02_rb,5.267846E-02_rb,5.091923E-02_rb,&
        & 4.926692E-02_rb,4.771154E-02_rb,4.623923E-02_rb,4.484385E-02_rb,4.351539E-02_rb,&
        & 4.224615E-02_rb,4.103385E-02_rb,3.986538E-02_rb,3.874077E-02_rb,3.765462E-02_rb,&
        & 3.660077E-02_rb,3.557384E-02_rb,3.457615E-02_rb,3.360308E-02_rb,3.265000E-02_rb,&
        & 3.171770E-02_rb,3.080538E-02_rb,2.990846E-02_rb,2.903000E-02_rb,2.816461E-02_rb,&
        & 2.731539E-02_rb,2.648231E-02_rb,2.566308E-02_rb,2.485923E-02_rb,2.407000E-02_rb,&
        & 2.329615E-02_rb,2.253769E-02_rb,2.179615E-02_rb /)
!     BAND  17
      extliq1(:, 17) = (/ &
       & 6.741200e-01_rb,5.390739e-01_rb,4.198767e-01_rb,3.332553e-01_rb,2.735633e-01_rb,&
       & 2.317727e-01_rb,2.012760e-01_rb,1.780400e-01_rb,1.596927e-01_rb,1.447980e-01_rb,&
       & 1.324480e-01_rb,1.220347e-01_rb,1.131327e-01_rb,1.054313e-01_rb,9.870534e-02_rb,&
       & 9.278200e-02_rb,8.752599e-02_rb,8.282933e-02_rb,7.860600e-02_rb,7.479133e-02_rb,&
       & 7.132800e-02_rb,6.816733e-02_rb,6.527401e-02_rb,6.261266e-02_rb,6.015934e-02_rb,&
       & 5.788867e-02_rb,5.578134e-02_rb,5.381667e-02_rb,5.198133e-02_rb,5.026067e-02_rb,&
       & 4.864466e-02_rb,4.712267e-02_rb,4.568066e-02_rb,4.431200e-02_rb,4.300867e-02_rb,&
       & 4.176600e-02_rb,4.057400e-02_rb,3.942534e-02_rb,3.832066e-02_rb,3.725068e-02_rb,&
       & 3.621400e-02_rb,3.520533e-02_rb,3.422333e-02_rb,3.326400e-02_rb,3.232467e-02_rb,&
       & 3.140535e-02_rb,3.050400e-02_rb,2.962000e-02_rb,2.875267e-02_rb,2.789800e-02_rb,&
       & 2.705934e-02_rb,2.623667e-02_rb,2.542667e-02_rb,2.463200e-02_rb,2.385267e-02_rb,&
       & 2.308667e-02_rb,2.233667e-02_rb,2.160067e-02_rb /)
!     BAND  18
      extliq1(:, 18) = (/ &
       & 9.250861e-01_rb,6.245692e-01_rb,4.347038e-01_rb,3.320208e-01_rb,2.714869e-01_rb,&
       & 2.309516e-01_rb,2.012592e-01_rb,1.783315e-01_rb,1.600369e-01_rb,1.451000e-01_rb,&
       & 1.326838e-01_rb,1.222069e-01_rb,1.132554e-01_rb,1.055146e-01_rb,9.876000e-02_rb,&
       & 9.281386e-02_rb,8.754000e-02_rb,8.283078e-02_rb,7.860077e-02_rb,7.477769e-02_rb,&
       & 7.130847e-02_rb,6.814461e-02_rb,6.524615e-02_rb,6.258462e-02_rb,6.012847e-02_rb,&
       & 5.785462e-02_rb,5.574231e-02_rb,5.378000e-02_rb,5.194461e-02_rb,5.022462e-02_rb,&
       & 4.860846e-02_rb,4.708462e-02_rb,4.564154e-02_rb,4.427462e-02_rb,4.297231e-02_rb,&
       & 4.172769e-02_rb,4.053693e-02_rb,3.939000e-02_rb,3.828462e-02_rb,3.721692e-02_rb,&
       & 3.618000e-02_rb,3.517077e-02_rb,3.418923e-02_rb,3.323077e-02_rb,3.229154e-02_rb,&
       & 3.137154e-02_rb,3.047154e-02_rb,2.959077e-02_rb,2.872308e-02_rb,2.786846e-02_rb,&
       & 2.703077e-02_rb,2.620923e-02_rb,2.540077e-02_rb,2.460615e-02_rb,2.382693e-02_rb,&
       & 2.306231e-02_rb,2.231231e-02_rb,2.157923e-02_rb /)
!     BAND  19
      extliq1(:, 19) = (/ &
       & 9.298960e-01_rb,5.776460e-01_rb,4.083450e-01_rb,3.211160e-01_rb,2.666390e-01_rb,&
       & 2.281990e-01_rb,1.993250e-01_rb,1.768080e-01_rb,1.587810e-01_rb,1.440390e-01_rb,&
       & 1.317720e-01_rb,1.214150e-01_rb,1.125540e-01_rb,1.048890e-01_rb,9.819600e-02_rb,&
       & 9.230201e-02_rb,8.706900e-02_rb,8.239698e-02_rb,7.819500e-02_rb,7.439899e-02_rb,&
       & 7.095300e-02_rb,6.780700e-02_rb,6.492900e-02_rb,6.228600e-02_rb,5.984600e-02_rb,&
       & 5.758599e-02_rb,5.549099e-02_rb,5.353801e-02_rb,5.171400e-02_rb,5.000500e-02_rb,&
       & 4.840000e-02_rb,4.688500e-02_rb,4.545100e-02_rb,4.409300e-02_rb,4.279700e-02_rb,&
       & 4.156100e-02_rb,4.037700e-02_rb,3.923800e-02_rb,3.813800e-02_rb,3.707600e-02_rb,&
       & 3.604500e-02_rb,3.504300e-02_rb,3.406500e-02_rb,3.310800e-02_rb,3.217700e-02_rb,&
       & 3.126600e-02_rb,3.036800e-02_rb,2.948900e-02_rb,2.862400e-02_rb,2.777500e-02_rb,&
       & 2.694200e-02_rb,2.612300e-02_rb,2.531700e-02_rb,2.452800e-02_rb,2.375100e-02_rb,&
       & 2.299100e-02_rb,2.224300e-02_rb,2.151201e-02_rb /)
!     BAND  20
      extliq1(:, 20) = (/ &
       & 8.780964e-01_rb,5.407031e-01_rb,3.961100e-01_rb,3.166645e-01_rb,2.640455e-01_rb,&
       & 2.261070e-01_rb,1.974820e-01_rb,1.751775e-01_rb,1.573415e-01_rb,1.427725e-01_rb,&
       & 1.306535e-01_rb,1.204195e-01_rb,1.116650e-01_rb,1.040915e-01_rb,9.747550e-02_rb,&
       & 9.164800e-02_rb,8.647649e-02_rb,8.185501e-02_rb,7.770200e-02_rb,7.394749e-02_rb,&
       & 7.053800e-02_rb,6.742700e-02_rb,6.457999e-02_rb,6.196149e-02_rb,5.954450e-02_rb,&
       & 5.730650e-02_rb,5.522949e-02_rb,5.329450e-02_rb,5.148500e-02_rb,4.979000e-02_rb,&
       & 4.819600e-02_rb,4.669301e-02_rb,4.527050e-02_rb,4.391899e-02_rb,4.263500e-02_rb,&
       & 4.140500e-02_rb,4.022850e-02_rb,3.909500e-02_rb,3.800199e-02_rb,3.694600e-02_rb,&
       & 3.592000e-02_rb,3.492250e-02_rb,3.395050e-02_rb,3.300150e-02_rb,3.207250e-02_rb,&
       & 3.116250e-02_rb,3.027100e-02_rb,2.939500e-02_rb,2.853500e-02_rb,2.768900e-02_rb,&
       & 2.686000e-02_rb,2.604350e-02_rb,2.524150e-02_rb,2.445350e-02_rb,2.368049e-02_rb,&
       & 2.292150e-02_rb,2.217800e-02_rb,2.144800e-02_rb /)
!     BAND  21
      extliq1(:, 21) = (/ &
       & 7.937480e-01_rb,5.123036e-01_rb,3.858181e-01_rb,3.099622e-01_rb,2.586829e-01_rb,&
       & 2.217587e-01_rb,1.939755e-01_rb,1.723397e-01_rb,1.550258e-01_rb,1.408600e-01_rb,&
       & 1.290545e-01_rb,1.190661e-01_rb,1.105039e-01_rb,1.030848e-01_rb,9.659387e-02_rb,&
       & 9.086775e-02_rb,8.577807e-02_rb,8.122452e-02_rb,7.712711e-02_rb,7.342193e-02_rb,&
       & 7.005387e-02_rb,6.697840e-02_rb,6.416000e-02_rb,6.156903e-02_rb,5.917484e-02_rb,&
       & 5.695807e-02_rb,5.489968e-02_rb,5.298097e-02_rb,5.118806e-02_rb,4.950645e-02_rb,&
       & 4.792710e-02_rb,4.643581e-02_rb,4.502484e-02_rb,4.368547e-02_rb,4.241001e-02_rb,&
       & 4.118936e-02_rb,4.002193e-02_rb,3.889711e-02_rb,3.781322e-02_rb,3.676387e-02_rb,&
       & 3.574549e-02_rb,3.475548e-02_rb,3.379033e-02_rb,3.284678e-02_rb,3.192420e-02_rb,&
       & 3.102032e-02_rb,3.013484e-02_rb,2.926258e-02_rb,2.840839e-02_rb,2.756742e-02_rb,&
       & 2.674258e-02_rb,2.593064e-02_rb,2.513258e-02_rb,2.435000e-02_rb,2.358064e-02_rb,&
       & 2.282581e-02_rb,2.208548e-02_rb,2.135936e-02_rb /)
!     BAND  22
      extliq1(:, 22) = (/ &
       & 7.533129e-01_rb,5.033129e-01_rb,3.811271e-01_rb,3.062757e-01_rb,2.558729e-01_rb,&
       & 2.196828e-01_rb,1.924372e-01_rb,1.711714e-01_rb,1.541086e-01_rb,1.401114e-01_rb,&
       & 1.284257e-01_rb,1.185200e-01_rb,1.100243e-01_rb,1.026529e-01_rb,9.620142e-02_rb,&
       & 9.050714e-02_rb,8.544428e-02_rb,8.091714e-02_rb,7.684000e-02_rb,7.315429e-02_rb,&
       & 6.980143e-02_rb,6.673999e-02_rb,6.394000e-02_rb,6.136000e-02_rb,5.897715e-02_rb,&
       & 5.677000e-02_rb,5.472285e-02_rb,5.281286e-02_rb,5.102858e-02_rb,4.935429e-02_rb,&
       & 4.778000e-02_rb,4.629714e-02_rb,4.489142e-02_rb,4.355857e-02_rb,4.228715e-02_rb,&
       & 4.107285e-02_rb,3.990857e-02_rb,3.879000e-02_rb,3.770999e-02_rb,3.666429e-02_rb,&
       & 3.565000e-02_rb,3.466286e-02_rb,3.370143e-02_rb,3.276143e-02_rb,3.184143e-02_rb,&
       & 3.094000e-02_rb,3.005714e-02_rb,2.919000e-02_rb,2.833714e-02_rb,2.750000e-02_rb,&
       & 2.667714e-02_rb,2.586714e-02_rb,2.507143e-02_rb,2.429143e-02_rb,2.352428e-02_rb,&
       & 2.277143e-02_rb,2.203429e-02_rb,2.130857e-02_rb /)
!     BAND  23
      extliq1(:, 23) = (/ &
       & 7.079894e-01_rb,4.878198e-01_rb,3.719852e-01_rb,3.001873e-01_rb,2.514795e-01_rb,&
       & 2.163013e-01_rb,1.897100e-01_rb,1.689033e-01_rb,1.521793e-01_rb,1.384449e-01_rb,&
       & 1.269666e-01_rb,1.172326e-01_rb,1.088745e-01_rb,1.016224e-01_rb,9.527085e-02_rb,&
       & 8.966240e-02_rb,8.467543e-02_rb,8.021144e-02_rb,7.619344e-02_rb,7.255676e-02_rb,&
       & 6.924996e-02_rb,6.623030e-02_rb,6.346261e-02_rb,6.091499e-02_rb,5.856325e-02_rb,&
       & 5.638385e-02_rb,5.435930e-02_rb,5.247156e-02_rb,5.070699e-02_rb,4.905230e-02_rb,&
       & 4.749499e-02_rb,4.602611e-02_rb,4.463581e-02_rb,4.331543e-02_rb,4.205647e-02_rb,&
       & 4.085241e-02_rb,3.969978e-02_rb,3.859033e-02_rb,3.751877e-02_rb,3.648168e-02_rb,&
       & 3.547468e-02_rb,3.449553e-02_rb,3.354072e-02_rb,3.260732e-02_rb,3.169438e-02_rb,&
       & 3.079969e-02_rb,2.992146e-02_rb,2.905875e-02_rb,2.821201e-02_rb,2.737873e-02_rb,&
       & 2.656052e-02_rb,2.575586e-02_rb,2.496511e-02_rb,2.418783e-02_rb,2.342500e-02_rb,&
       & 2.267646e-02_rb,2.194177e-02_rb,2.122146e-02_rb /)
!     BAND  24
      extliq1(:, 24) = (/ &
       & 6.850164e-01_rb,4.762468e-01_rb,3.642001e-01_rb,2.946012e-01_rb,2.472001e-01_rb,&
       & 2.128588e-01_rb,1.868537e-01_rb,1.664893e-01_rb,1.501142e-01_rb,1.366620e-01_rb,&
       & 1.254147e-01_rb,1.158721e-01_rb,1.076732e-01_rb,1.005530e-01_rb,9.431306e-02_rb,&
       & 8.879891e-02_rb,8.389232e-02_rb,7.949714e-02_rb,7.553857e-02_rb,7.195474e-02_rb,&
       & 6.869413e-02_rb,6.571444e-02_rb,6.298286e-02_rb,6.046779e-02_rb,5.814474e-02_rb,&
       & 5.599141e-02_rb,5.399114e-02_rb,5.212443e-02_rb,5.037870e-02_rb,4.874321e-02_rb,&
       & 4.720219e-02_rb,4.574813e-02_rb,4.437160e-02_rb,4.306460e-02_rb,4.181810e-02_rb,&
       & 4.062603e-02_rb,3.948252e-02_rb,3.838256e-02_rb,3.732049e-02_rb,3.629192e-02_rb,&
       & 3.529301e-02_rb,3.432190e-02_rb,3.337412e-02_rb,3.244842e-02_rb,3.154175e-02_rb,&
       & 3.065253e-02_rb,2.978063e-02_rb,2.892367e-02_rb,2.808221e-02_rb,2.725478e-02_rb,&
       & 2.644174e-02_rb,2.564175e-02_rb,2.485508e-02_rb,2.408303e-02_rb,2.332365e-02_rb,&
       & 2.257890e-02_rb,2.184824e-02_rb,2.113224e-02_rb /)
!     BAND  25
      extliq1(:, 25) = (/ &
       & 6.673017e-01_rb,4.664520e-01_rb,3.579398e-01_rb,2.902234e-01_rb,2.439904e-01_rb,&
       & 2.104149e-01_rb,1.849277e-01_rb,1.649234e-01_rb,1.488087e-01_rb,1.355515e-01_rb,&
       & 1.244562e-01_rb,1.150329e-01_rb,1.069321e-01_rb,9.989310e-02_rb,9.372070e-02_rb,&
       & 8.826450e-02_rb,8.340622e-02_rb,7.905378e-02_rb,7.513109e-02_rb,7.157859e-02_rb,&
       & 6.834588e-02_rb,6.539114e-02_rb,6.268150e-02_rb,6.018621e-02_rb,5.788098e-02_rb,&
       & 5.574351e-02_rb,5.375699e-02_rb,5.190412e-02_rb,5.017099e-02_rb,4.854497e-02_rb,&
       & 4.701490e-02_rb,4.557030e-02_rb,4.420249e-02_rb,4.290304e-02_rb,4.166427e-02_rb,&
       & 4.047820e-02_rb,3.934232e-02_rb,3.824778e-02_rb,3.719236e-02_rb,3.616931e-02_rb,&
       & 3.517597e-02_rb,3.420856e-02_rb,3.326566e-02_rb,3.234346e-02_rb,3.144122e-02_rb,&
       & 3.055684e-02_rb,2.968798e-02_rb,2.883519e-02_rb,2.799635e-02_rb,2.717228e-02_rb,&
       & 2.636182e-02_rb,2.556424e-02_rb,2.478114e-02_rb,2.401086e-02_rb,2.325657e-02_rb,&
       & 2.251506e-02_rb,2.178594e-02_rb,2.107301e-02_rb /)
!     BAND  26
      extliq1(:, 26) = (/ &
       & 6.552414e-01_rb,4.599454e-01_rb,3.538626e-01_rb,2.873547e-01_rb,2.418033e-01_rb,&
       & 2.086660e-01_rb,1.834885e-01_rb,1.637142e-01_rb,1.477767e-01_rb,1.346583e-01_rb,&
       & 1.236734e-01_rb,1.143412e-01_rb,1.063148e-01_rb,9.933905e-02_rb,9.322026e-02_rb,&
       & 8.780979e-02_rb,8.299230e-02_rb,7.867554e-02_rb,7.478450e-02_rb,7.126053e-02_rb,&
       & 6.805276e-02_rb,6.512143e-02_rb,6.243211e-02_rb,5.995541e-02_rb,5.766712e-02_rb,&
       & 5.554484e-02_rb,5.357246e-02_rb,5.173222e-02_rb,5.001069e-02_rb,4.839505e-02_rb,&
       & 4.687471e-02_rb,4.543861e-02_rb,4.407857e-02_rb,4.278577e-02_rb,4.155331e-02_rb,&
       & 4.037322e-02_rb,3.924302e-02_rb,3.815376e-02_rb,3.710172e-02_rb,3.608296e-02_rb,&
       & 3.509330e-02_rb,3.412980e-02_rb,3.319009e-02_rb,3.227106e-02_rb,3.137157e-02_rb,&
       & 3.048950e-02_rb,2.962365e-02_rb,2.877297e-02_rb,2.793726e-02_rb,2.711500e-02_rb,&
       & 2.630666e-02_rb,2.551206e-02_rb,2.473052e-02_rb,2.396287e-02_rb,2.320861e-02_rb,&
       & 2.246810e-02_rb,2.174162e-02_rb,2.102927e-02_rb /)
!     BAND  27
      extliq1(:, 27) = (/ &
       & 6.430901e-01_rb,4.532134e-01_rb,3.496132e-01_rb,2.844655e-01_rb,2.397347e-01_rb,&
       & 2.071236e-01_rb,1.822976e-01_rb,1.627640e-01_rb,1.469961e-01_rb,1.340006e-01_rb,&
       & 1.231069e-01_rb,1.138441e-01_rb,1.058706e-01_rb,9.893678e-02_rb,9.285166e-02_rb,&
       & 8.746871e-02_rb,8.267411e-02_rb,7.837656e-02_rb,7.450257e-02_rb,7.099318e-02_rb,&
       & 6.779929e-02_rb,6.487987e-02_rb,6.220168e-02_rb,5.973530e-02_rb,5.745636e-02_rb,&
       & 5.534344e-02_rb,5.337986e-02_rb,5.154797e-02_rb,4.983404e-02_rb,4.822582e-02_rb,&
       & 4.671228e-02_rb,4.528321e-02_rb,4.392997e-02_rb,4.264325e-02_rb,4.141647e-02_rb,&
       & 4.024259e-02_rb,3.911767e-02_rb,3.803309e-02_rb,3.698782e-02_rb,3.597140e-02_rb,&
       & 3.498774e-02_rb,3.402852e-02_rb,3.309340e-02_rb,3.217818e-02_rb,3.128292e-02_rb,&
       & 3.040486e-02_rb,2.954230e-02_rb,2.869545e-02_rb,2.786261e-02_rb,2.704372e-02_rb,&
       & 2.623813e-02_rb,2.544668e-02_rb,2.466788e-02_rb,2.390313e-02_rb,2.315136e-02_rb,&
       & 2.241391e-02_rb,2.168921e-02_rb,2.097903e-02_rb /)
!     BAND  28
      extliq1(:, 28) = (/ &
       & 6.367074e-01_rb,4.495768e-01_rb,3.471263e-01_rb,2.826149e-01_rb,2.382868e-01_rb,&
       & 2.059640e-01_rb,1.813562e-01_rb,1.619881e-01_rb,1.463436e-01_rb,1.334402e-01_rb,&
       & 1.226166e-01_rb,1.134096e-01_rb,1.054829e-01_rb,9.858838e-02_rb,9.253790e-02_rb,&
       & 8.718582e-02_rb,8.241830e-02_rb,7.814482e-02_rb,7.429212e-02_rb,7.080165e-02_rb,&
       & 6.762385e-02_rb,6.471838e-02_rb,6.205388e-02_rb,5.959726e-02_rb,5.732871e-02_rb,&
       & 5.522402e-02_rb,5.326793e-02_rb,5.144230e-02_rb,4.973440e-02_rb,4.813188e-02_rb,&
       & 4.662283e-02_rb,4.519798e-02_rb,4.384833e-02_rb,4.256541e-02_rb,4.134253e-02_rb,&
       & 4.017136e-02_rb,3.904911e-02_rb,3.796779e-02_rb,3.692364e-02_rb,3.591182e-02_rb,&
       & 3.492930e-02_rb,3.397230e-02_rb,3.303920e-02_rb,3.212572e-02_rb,3.123278e-02_rb,&
       & 3.035519e-02_rb,2.949493e-02_rb,2.864985e-02_rb,2.781840e-02_rb,2.700197e-02_rb,&
       & 2.619682e-02_rb,2.540674e-02_rb,2.462966e-02_rb,2.386613e-02_rb,2.311602e-02_rb,&
       & 2.237846e-02_rb,2.165660e-02_rb,2.094756e-02_rb /)
!     BAND  29
      extliq1(:, 29) = (/ &
       & 4.298416e-01_rb,4.391639e-01_rb,3.975030e-01_rb,3.443028e-01_rb,2.957345e-01_rb,&
       & 2.556461e-01_rb,2.234755e-01_rb,1.976636e-01_rb,1.767428e-01_rb,1.595611e-01_rb,&
       & 1.452636e-01_rb,1.332156e-01_rb,1.229481e-01_rb,1.141059e-01_rb,1.064208e-01_rb,&
       & 9.968527e-02_rb,9.373833e-02_rb,8.845221e-02_rb,8.372112e-02_rb,7.946667e-02_rb,&
       & 7.561807e-02_rb,7.212029e-02_rb,6.893166e-02_rb,6.600944e-02_rb,6.332277e-02_rb,&
       & 6.084277e-02_rb,5.854721e-02_rb,5.641361e-02_rb,5.442639e-02_rb,5.256750e-02_rb,&
       & 5.082499e-02_rb,4.918556e-02_rb,4.763694e-02_rb,4.617222e-02_rb,4.477861e-02_rb,&
       & 4.344861e-02_rb,4.217999e-02_rb,4.096111e-02_rb,3.978638e-02_rb,3.865361e-02_rb,&
       & 3.755473e-02_rb,3.649028e-02_rb,3.545361e-02_rb,3.444361e-02_rb,3.345666e-02_rb,&
       & 3.249167e-02_rb,3.154722e-02_rb,3.062083e-02_rb,2.971250e-02_rb,2.882083e-02_rb,&
       & 2.794611e-02_rb,2.708778e-02_rb,2.624500e-02_rb,2.541750e-02_rb,2.460528e-02_rb,&
       & 2.381194e-02_rb,2.303250e-02_rb,2.226833e-02_rb /)
!     BAND  16
      ssaliq1(:, 16) = (/ &
       & 8.362119e-01_rb,8.098460e-01_rb,7.762291e-01_rb,7.486042e-01_rb,7.294172e-01_rb,&
       & 7.161000e-01_rb,7.060656e-01_rb,6.978387e-01_rb,6.907193e-01_rb,6.843551e-01_rb,&
       & 6.785668e-01_rb,6.732450e-01_rb,6.683191e-01_rb,6.637264e-01_rb,6.594307e-01_rb,&
       & 6.554033e-01_rb,6.516115e-01_rb,6.480295e-01_rb,6.446429e-01_rb,6.414306e-01_rb,&
       & 6.383783e-01_rb,6.354750e-01_rb,6.327068e-01_rb,6.300665e-01_rb,6.275376e-01_rb,&
       & 6.251245e-01_rb,6.228136e-01_rb,6.205944e-01_rb,6.184720e-01_rb,6.164330e-01_rb,&
       & 6.144742e-01_rb,6.125962e-01_rb,6.108004e-01_rb,6.090740e-01_rb,6.074200e-01_rb,&
       & 6.058381e-01_rb,6.043209e-01_rb,6.028681e-01_rb,6.014836e-01_rb,6.001626e-01_rb,&
       & 5.988957e-01_rb,5.976864e-01_rb,5.965390e-01_rb,5.954379e-01_rb,5.943972e-01_rb,&
       & 5.934019e-01_rb,5.924624e-01_rb,5.915579e-01_rb,5.907025e-01_rb,5.898913e-01_rb,&
       & 5.891213e-01_rb,5.883815e-01_rb,5.876851e-01_rb,5.870158e-01_rb,5.863868e-01_rb,&
       & 5.857821e-01_rb,5.852111e-01_rb,5.846579e-01_rb /)
!     BAND  17
      ssaliq1(:, 17) = (/ &
       & 6.995459e-01_rb,7.158012e-01_rb,7.076001e-01_rb,6.927244e-01_rb,6.786434e-01_rb,&
       & 6.673545e-01_rb,6.585859e-01_rb,6.516314e-01_rb,6.459010e-01_rb,6.410225e-01_rb,&
       & 6.367574e-01_rb,6.329554e-01_rb,6.295119e-01_rb,6.263595e-01_rb,6.234462e-01_rb,&
       & 6.207274e-01_rb,6.181755e-01_rb,6.157678e-01_rb,6.134880e-01_rb,6.113173e-01_rb,&
       & 6.092495e-01_rb,6.072689e-01_rb,6.053717e-01_rb,6.035507e-01_rb,6.018001e-01_rb,&
       & 6.001134e-01_rb,5.984951e-01_rb,5.969294e-01_rb,5.954256e-01_rb,5.939698e-01_rb,&
       & 5.925716e-01_rb,5.912265e-01_rb,5.899270e-01_rb,5.886771e-01_rb,5.874746e-01_rb,&
       & 5.863185e-01_rb,5.852077e-01_rb,5.841460e-01_rb,5.831249e-01_rb,5.821474e-01_rb,&
       & 5.812078e-01_rb,5.803173e-01_rb,5.794616e-01_rb,5.786443e-01_rb,5.778617e-01_rb,&
       & 5.771236e-01_rb,5.764191e-01_rb,5.757400e-01_rb,5.750971e-01_rb,5.744842e-01_rb,&
       & 5.739012e-01_rb,5.733482e-01_rb,5.728175e-01_rb,5.723214e-01_rb,5.718383e-01_rb,&
       & 5.713827e-01_rb,5.709471e-01_rb,5.705330e-01_rb /)
!     BAND  18
      ssaliq1(:, 18) = (/ &
       & 9.929711e-01_rb,9.896942e-01_rb,9.852408e-01_rb,9.806820e-01_rb,9.764512e-01_rb,&
       & 9.725375e-01_rb,9.688677e-01_rb,9.653832e-01_rb,9.620552e-01_rb,9.588522e-01_rb,&
       & 9.557475e-01_rb,9.527265e-01_rb,9.497731e-01_rb,9.468756e-01_rb,9.440270e-01_rb,&
       & 9.412230e-01_rb,9.384592e-01_rb,9.357287e-01_rb,9.330369e-01_rb,9.303778e-01_rb,&
       & 9.277502e-01_rb,9.251546e-01_rb,9.225907e-01_rb,9.200553e-01_rb,9.175521e-01_rb,&
       & 9.150773e-01_rb,9.126352e-01_rb,9.102260e-01_rb,9.078485e-01_rb,9.055057e-01_rb,&
       & 9.031978e-01_rb,9.009306e-01_rb,8.987010e-01_rb,8.965177e-01_rb,8.943774e-01_rb,&
       & 8.922869e-01_rb,8.902430e-01_rb,8.882551e-01_rb,8.863182e-01_rb,8.844373e-01_rb,&
       & 8.826143e-01_rb,8.808499e-01_rb,8.791413e-01_rb,8.774940e-01_rb,8.759019e-01_rb,&
       & 8.743650e-01_rb,8.728941e-01_rb,8.714712e-01_rb,8.701065e-01_rb,8.688008e-01_rb,&
       & 8.675409e-01_rb,8.663295e-01_rb,8.651714e-01_rb,8.640637e-01_rb,8.629943e-01_rb,&
       & 8.619762e-01_rb,8.609995e-01_rb,8.600581e-01_rb /)
!     BAND  19
      ssaliq1(:, 19) = (/ &
       & 9.910612e-01_rb,9.854226e-01_rb,9.795008e-01_rb,9.742920e-01_rb,9.695996e-01_rb,&
       & 9.652274e-01_rb,9.610648e-01_rb,9.570521e-01_rb,9.531397e-01_rb,9.493086e-01_rb,&
       & 9.455413e-01_rb,9.418362e-01_rb,9.381902e-01_rb,9.346016e-01_rb,9.310718e-01_rb,&
       & 9.275957e-01_rb,9.241757e-01_rb,9.208038e-01_rb,9.174802e-01_rb,9.142058e-01_rb,&
       & 9.109753e-01_rb,9.077895e-01_rb,9.046433e-01_rb,9.015409e-01_rb,8.984784e-01_rb,&
       & 8.954572e-01_rb,8.924748e-01_rb,8.895367e-01_rb,8.866395e-01_rb,8.837864e-01_rb,&
       & 8.809819e-01_rb,8.782267e-01_rb,8.755231e-01_rb,8.728712e-01_rb,8.702802e-01_rb,&
       & 8.677443e-01_rb,8.652733e-01_rb,8.628678e-01_rb,8.605300e-01_rb,8.582593e-01_rb,&
       & 8.560596e-01_rb,8.539352e-01_rb,8.518782e-01_rb,8.498915e-01_rb,8.479790e-01_rb,&
       & 8.461384e-01_rb,8.443645e-01_rb,8.426613e-01_rb,8.410229e-01_rb,8.394495e-01_rb,&
       & 8.379428e-01_rb,8.364967e-01_rb,8.351117e-01_rb,8.337820e-01_rb,8.325091e-01_rb,&
       & 8.312874e-01_rb,8.301169e-01_rb,8.289985e-01_rb /)
!     BAND  20
      ssaliq1(:, 20) = (/ &
       & 9.969802e-01_rb,9.950445e-01_rb,9.931448e-01_rb,9.914272e-01_rb,9.898652e-01_rb,&
       & 9.884250e-01_rb,9.870637e-01_rb,9.857482e-01_rb,9.844558e-01_rb,9.831755e-01_rb,&
       & 9.819068e-01_rb,9.806477e-01_rb,9.794000e-01_rb,9.781666e-01_rb,9.769461e-01_rb,&
       & 9.757386e-01_rb,9.745459e-01_rb,9.733650e-01_rb,9.721953e-01_rb,9.710398e-01_rb,&
       & 9.698936e-01_rb,9.687583e-01_rb,9.676334e-01_rb,9.665192e-01_rb,9.654132e-01_rb,&
       & 9.643208e-01_rb,9.632374e-01_rb,9.621625e-01_rb,9.611003e-01_rb,9.600518e-01_rb,&
       & 9.590144e-01_rb,9.579922e-01_rb,9.569864e-01_rb,9.559948e-01_rb,9.550239e-01_rb,&
       & 9.540698e-01_rb,9.531382e-01_rb,9.522280e-01_rb,9.513409e-01_rb,9.504772e-01_rb,&
       & 9.496360e-01_rb,9.488220e-01_rb,9.480327e-01_rb,9.472693e-01_rb,9.465333e-01_rb,&
       & 9.458211e-01_rb,9.451344e-01_rb,9.444732e-01_rb,9.438372e-01_rb,9.432268e-01_rb,&
       & 9.426391e-01_rb,9.420757e-01_rb,9.415308e-01_rb,9.410102e-01_rb,9.405115e-01_rb,&
       & 9.400326e-01_rb,9.395716e-01_rb,9.391313e-01_rb /)
!     BAND  21
      ssaliq1(:, 21) = (/ &
       & 9.980034e-01_rb,9.968572e-01_rb,9.958696e-01_rb,9.949747e-01_rb,9.941241e-01_rb,&
       & 9.933043e-01_rb,9.924971e-01_rb,9.916978e-01_rb,9.909023e-01_rb,9.901046e-01_rb,&
       & 9.893087e-01_rb,9.885146e-01_rb,9.877195e-01_rb,9.869283e-01_rb,9.861379e-01_rb,&
       & 9.853523e-01_rb,9.845715e-01_rb,9.837945e-01_rb,9.830217e-01_rb,9.822567e-01_rb,&
       & 9.814935e-01_rb,9.807356e-01_rb,9.799815e-01_rb,9.792332e-01_rb,9.784845e-01_rb,&
       & 9.777424e-01_rb,9.770042e-01_rb,9.762695e-01_rb,9.755416e-01_rb,9.748152e-01_rb,&
       & 9.740974e-01_rb,9.733873e-01_rb,9.726813e-01_rb,9.719861e-01_rb,9.713010e-01_rb,&
       & 9.706262e-01_rb,9.699647e-01_rb,9.693144e-01_rb,9.686794e-01_rb,9.680596e-01_rb,&
       & 9.674540e-01_rb,9.668657e-01_rb,9.662926e-01_rb,9.657390e-01_rb,9.652019e-01_rb,&
       & 9.646820e-01_rb,9.641784e-01_rb,9.636945e-01_rb,9.632260e-01_rb,9.627743e-01_rb,&
       & 9.623418e-01_rb,9.619227e-01_rb,9.615194e-01_rb,9.611341e-01_rb,9.607629e-01_rb,&
       & 9.604057e-01_rb,9.600622e-01_rb,9.597322e-01_rb /)
!     BAND  22
      ssaliq1(:, 22) = (/ &
       & 9.988219e-01_rb,9.981767e-01_rb,9.976168e-01_rb,9.971066e-01_rb,9.966195e-01_rb,&
       & 9.961566e-01_rb,9.956995e-01_rb,9.952481e-01_rb,9.947982e-01_rb,9.943495e-01_rb,&
       & 9.938955e-01_rb,9.934368e-01_rb,9.929825e-01_rb,9.925239e-01_rb,9.920653e-01_rb,&
       & 9.916096e-01_rb,9.911552e-01_rb,9.907067e-01_rb,9.902594e-01_rb,9.898178e-01_rb,&
       & 9.893791e-01_rb,9.889453e-01_rb,9.885122e-01_rb,9.880837e-01_rb,9.876567e-01_rb,&
       & 9.872331e-01_rb,9.868121e-01_rb,9.863938e-01_rb,9.859790e-01_rb,9.855650e-01_rb,&
       & 9.851548e-01_rb,9.847491e-01_rb,9.843496e-01_rb,9.839521e-01_rb,9.835606e-01_rb,&
       & 9.831771e-01_rb,9.827975e-01_rb,9.824292e-01_rb,9.820653e-01_rb,9.817124e-01_rb,&
       & 9.813644e-01_rb,9.810291e-01_rb,9.807020e-01_rb,9.803864e-01_rb,9.800782e-01_rb,&
       & 9.797821e-01_rb,9.794958e-01_rb,9.792179e-01_rb,9.789509e-01_rb,9.786940e-01_rb,&
       & 9.784460e-01_rb,9.782090e-01_rb,9.779789e-01_rb,9.777553e-01_rb,9.775425e-01_rb,&
       & 9.773387e-01_rb,9.771420e-01_rb,9.769529e-01_rb /)
!     BAND  23
      ssaliq1(:, 23) = (/ &
       & 9.998902e-01_rb,9.998395e-01_rb,9.997915e-01_rb,9.997442e-01_rb,9.997016e-01_rb,&
       & 9.996600e-01_rb,9.996200e-01_rb,9.995806e-01_rb,9.995411e-01_rb,9.995005e-01_rb,&
       & 9.994589e-01_rb,9.994178e-01_rb,9.993766e-01_rb,9.993359e-01_rb,9.992948e-01_rb,&
       & 9.992533e-01_rb,9.992120e-01_rb,9.991723e-01_rb,9.991313e-01_rb,9.990906e-01_rb,&
       & 9.990510e-01_rb,9.990113e-01_rb,9.989716e-01_rb,9.989323e-01_rb,9.988923e-01_rb,&
       & 9.988532e-01_rb,9.988140e-01_rb,9.987761e-01_rb,9.987373e-01_rb,9.986989e-01_rb,&
       & 9.986597e-01_rb,9.986239e-01_rb,9.985861e-01_rb,9.985485e-01_rb,9.985123e-01_rb,&
       & 9.984762e-01_rb,9.984415e-01_rb,9.984065e-01_rb,9.983722e-01_rb,9.983398e-01_rb,&
       & 9.983078e-01_rb,9.982758e-01_rb,9.982461e-01_rb,9.982157e-01_rb,9.981872e-01_rb,&
       & 9.981595e-01_rb,9.981324e-01_rb,9.981068e-01_rb,9.980811e-01_rb,9.980580e-01_rb,&
       & 9.980344e-01_rb,9.980111e-01_rb,9.979908e-01_rb,9.979690e-01_rb,9.979492e-01_rb,&
       & 9.979316e-01_rb,9.979116e-01_rb,9.978948e-01_rb /)
!     BAND  24
      ssaliq1(:, 24) = (/ &
       & 9.999978e-01_rb,9.999948e-01_rb,9.999915e-01_rb,9.999905e-01_rb,9.999896e-01_rb,&
       & 9.999887e-01_rb,9.999888e-01_rb,9.999888e-01_rb,9.999870e-01_rb,9.999854e-01_rb,&
       & 9.999855e-01_rb,9.999856e-01_rb,9.999839e-01_rb,9.999834e-01_rb,9.999829e-01_rb,&
       & 9.999809e-01_rb,9.999816e-01_rb,9.999793e-01_rb,9.999782e-01_rb,9.999779e-01_rb,&
       & 9.999772e-01_rb,9.999764e-01_rb,9.999756e-01_rb,9.999744e-01_rb,9.999744e-01_rb,&
       & 9.999736e-01_rb,9.999729e-01_rb,9.999716e-01_rb,9.999706e-01_rb,9.999692e-01_rb,&
       & 9.999690e-01_rb,9.999675e-01_rb,9.999673e-01_rb,9.999660e-01_rb,9.999654e-01_rb,&
       & 9.999647e-01_rb,9.999647e-01_rb,9.999625e-01_rb,9.999620e-01_rb,9.999614e-01_rb,&
       & 9.999613e-01_rb,9.999607e-01_rb,9.999604e-01_rb,9.999594e-01_rb,9.999589e-01_rb,&
       & 9.999586e-01_rb,9.999567e-01_rb,9.999550e-01_rb,9.999557e-01_rb,9.999542e-01_rb,&
       & 9.999546e-01_rb,9.999539e-01_rb,9.999536e-01_rb,9.999526e-01_rb,9.999523e-01_rb,&
       & 9.999508e-01_rb,9.999534e-01_rb,9.999507e-01_rb /)
!     BAND  25
      ssaliq1(:, 25) = (/ &
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,&
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,&
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,&
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,9.999995e-01_rb,&
       & 9.999995e-01_rb,9.999990e-01_rb,9.999991e-01_rb,9.999991e-01_rb,9.999990e-01_rb,&
       & 9.999989e-01_rb,9.999988e-01_rb,9.999988e-01_rb,9.999986e-01_rb,9.999988e-01_rb,&
       & 9.999986e-01_rb,9.999987e-01_rb,9.999986e-01_rb,9.999985e-01_rb,9.999985e-01_rb,&
       & 9.999985e-01_rb,9.999985e-01_rb,9.999983e-01_rb,9.999983e-01_rb,9.999981e-01_rb,&
       & 9.999981e-01_rb,9.999986e-01_rb,9.999985e-01_rb,9.999983e-01_rb,9.999984e-01_rb,&
       & 9.999982e-01_rb,9.999983e-01_rb,9.999982e-01_rb,9.999980e-01_rb,9.999981e-01_rb,&
       & 9.999978e-01_rb,9.999979e-01_rb,9.999985e-01_rb,9.999985e-01_rb,9.999983e-01_rb,&
       & 9.999983e-01_rb,9.999983e-01_rb,9.999983e-01_rb /)
!     BAND  26
      ssaliq1(:, 26) = (/ &
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,&
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,&
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,&
       & 1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,1.000000e+00_rb,9.999991e-01_rb,&
       & 9.999990e-01_rb,9.999992e-01_rb,9.999995e-01_rb,9.999986e-01_rb,9.999994e-01_rb,&
       & 9.999985e-01_rb,9.999980e-01_rb,9.999984e-01_rb,9.999983e-01_rb,9.999979e-01_rb,&
       & 9.999969e-01_rb,9.999977e-01_rb,9.999971e-01_rb,9.999969e-01_rb,9.999969e-01_rb,&
       & 9.999965e-01_rb,9.999970e-01_rb,9.999985e-01_rb,9.999973e-01_rb,9.999961e-01_rb,&
       & 9.999968e-01_rb,9.999952e-01_rb,9.999970e-01_rb,9.999974e-01_rb,9.999965e-01_rb,&
       & 9.999969e-01_rb,9.999970e-01_rb,9.999970e-01_rb,9.999960e-01_rb,9.999923e-01_rb,&
       & 9.999958e-01_rb,9.999937e-01_rb,9.999960e-01_rb,9.999953e-01_rb,9.999946e-01_rb,&
       & 9.999946e-01_rb,9.999957e-01_rb,9.999951e-01_rb /)
!     BAND  27
      ssaliq1(:, 27) = (/ &
       & 1.000000e+00_rb,1.000000e+00_rb,9.999983e-01_rb,9.999979e-01_rb,9.999965e-01_rb,&
       & 9.999949e-01_rb,9.999948e-01_rb,9.999918e-01_rb,9.999917e-01_rb,9.999923e-01_rb,&
       & 9.999908e-01_rb,9.999889e-01_rb,9.999902e-01_rb,9.999895e-01_rb,9.999881e-01_rb,&
       & 9.999882e-01_rb,9.999876e-01_rb,9.999866e-01_rb,9.999866e-01_rb,9.999858e-01_rb,&
       & 9.999860e-01_rb,9.999852e-01_rb,9.999836e-01_rb,9.999831e-01_rb,9.999818e-01_rb,&
       & 9.999808e-01_rb,9.999816e-01_rb,9.999800e-01_rb,9.999783e-01_rb,9.999780e-01_rb,&
       & 9.999763e-01_rb,9.999746e-01_rb,9.999731e-01_rb,9.999713e-01_rb,9.999762e-01_rb,&
       & 9.999740e-01_rb,9.999670e-01_rb,9.999703e-01_rb,9.999687e-01_rb,9.999666e-01_rb,&
       & 9.999683e-01_rb,9.999667e-01_rb,9.999611e-01_rb,9.999635e-01_rb,9.999600e-01_rb,&
       & 9.999635e-01_rb,9.999594e-01_rb,9.999601e-01_rb,9.999586e-01_rb,9.999559e-01_rb,&
       & 9.999569e-01_rb,9.999558e-01_rb,9.999523e-01_rb,9.999535e-01_rb,9.999529e-01_rb,&
       & 9.999553e-01_rb,9.999495e-01_rb,9.999490e-01_rb /)
!     BAND  28
      ssaliq1(:, 28) = (/ &
       & 9.999920e-01_rb,9.999873e-01_rb,9.999855e-01_rb,9.999832e-01_rb,9.999807e-01_rb,&
       & 9.999778e-01_rb,9.999754e-01_rb,9.999721e-01_rb,9.999692e-01_rb,9.999651e-01_rb,&
       & 9.999621e-01_rb,9.999607e-01_rb,9.999567e-01_rb,9.999546e-01_rb,9.999521e-01_rb,&
       & 9.999491e-01_rb,9.999457e-01_rb,9.999439e-01_rb,9.999403e-01_rb,9.999374e-01_rb,&
       & 9.999353e-01_rb,9.999315e-01_rb,9.999282e-01_rb,9.999244e-01_rb,9.999234e-01_rb,&
       & 9.999189e-01_rb,9.999130e-01_rb,9.999117e-01_rb,9.999073e-01_rb,9.999020e-01_rb,&
       & 9.998993e-01_rb,9.998987e-01_rb,9.998922e-01_rb,9.998893e-01_rb,9.998869e-01_rb,&
       & 9.998805e-01_rb,9.998778e-01_rb,9.998751e-01_rb,9.998708e-01_rb,9.998676e-01_rb,&
       & 9.998624e-01_rb,9.998642e-01_rb,9.998582e-01_rb,9.998547e-01_rb,9.998546e-01_rb,&
       & 9.998477e-01_rb,9.998487e-01_rb,9.998466e-01_rb,9.998403e-01_rb,9.998412e-01_rb,&
       & 9.998406e-01_rb,9.998342e-01_rb,9.998326e-01_rb,9.998333e-01_rb,9.998328e-01_rb,&
       & 9.998290e-01_rb,9.998276e-01_rb,9.998249e-01_rb /)
!     BAND  29
      ssaliq1(:, 29) = (/ &
       & 8.383753e-01_rb,8.461471e-01_rb,8.373325e-01_rb,8.212889e-01_rb,8.023834e-01_rb,&
       & 7.829501e-01_rb,7.641777e-01_rb,7.466000e-01_rb,7.304023e-01_rb,7.155998e-01_rb,&
       & 7.021259e-01_rb,6.898840e-01_rb,6.787615e-01_rb,6.686479e-01_rb,6.594414e-01_rb,&
       & 6.510417e-01_rb,6.433668e-01_rb,6.363335e-01_rb,6.298788e-01_rb,6.239398e-01_rb,&
       & 6.184633e-01_rb,6.134055e-01_rb,6.087228e-01_rb,6.043786e-01_rb,6.003439e-01_rb,&
       & 5.965910e-01_rb,5.930917e-01_rb,5.898280e-01_rb,5.867798e-01_rb,5.839264e-01_rb,&
       & 5.812576e-01_rb,5.787592e-01_rb,5.764163e-01_rb,5.742189e-01_rb,5.721598e-01_rb,&
       & 5.702286e-01_rb,5.684182e-01_rb,5.667176e-01_rb,5.651237e-01_rb,5.636253e-01_rb,&
       & 5.622228e-01_rb,5.609074e-01_rb,5.596713e-01_rb,5.585089e-01_rb,5.574223e-01_rb,&
       & 5.564002e-01_rb,5.554411e-01_rb,5.545397e-01_rb,5.536914e-01_rb,5.528967e-01_rb,&
       & 5.521495e-01_rb,5.514457e-01_rb,5.507818e-01_rb,5.501623e-01_rb,5.495750e-01_rb,&
       & 5.490192e-01_rb,5.484980e-01_rb,5.480046e-01_rb /)
!     BAND  16
      asyliq1(:, 16) = (/ &
       & 8.038165e-01_rb,8.014154e-01_rb,7.942381e-01_rb,7.970521e-01_rb,8.086621e-01_rb,&
       & 8.233392e-01_rb,8.374127e-01_rb,8.495742e-01_rb,8.596945e-01_rb,8.680497e-01_rb,&
       & 8.750005e-01_rb,8.808589e-01_rb,8.858749e-01_rb,8.902403e-01_rb,8.940939e-01_rb,&
       & 8.975379e-01_rb,9.006450e-01_rb,9.034741e-01_rb,9.060659e-01_rb,9.084561e-01_rb,&
       & 9.106675e-01_rb,9.127198e-01_rb,9.146332e-01_rb,9.164194e-01_rb,9.180970e-01_rb,&
       & 9.196658e-01_rb,9.211421e-01_rb,9.225352e-01_rb,9.238443e-01_rb,9.250841e-01_rb,&
       & 9.262541e-01_rb,9.273620e-01_rb,9.284081e-01_rb,9.294002e-01_rb,9.303395e-01_rb,&
       & 9.312285e-01_rb,9.320715e-01_rb,9.328716e-01_rb,9.336271e-01_rb,9.343427e-01_rb,&
       & 9.350219e-01_rb,9.356647e-01_rb,9.362728e-01_rb,9.368495e-01_rb,9.373956e-01_rb,&
       & 9.379113e-01_rb,9.383987e-01_rb,9.388608e-01_rb,9.392986e-01_rb,9.397132e-01_rb,&
       & 9.401063e-01_rb,9.404776e-01_rb,9.408299e-01_rb,9.411641e-01_rb,9.414800e-01_rb,&
       & 9.417787e-01_rb,9.420633e-01_rb,9.423364e-01_rb /)
!     BAND  17
      asyliq1(:, 17) = (/ &
       & 8.941000e-01_rb,9.054049e-01_rb,9.049510e-01_rb,9.027216e-01_rb,9.021636e-01_rb,&
       & 9.037878e-01_rb,9.069852e-01_rb,9.109817e-01_rb,9.152013e-01_rb,9.193040e-01_rb,&
       & 9.231177e-01_rb,9.265712e-01_rb,9.296606e-01_rb,9.324048e-01_rb,9.348419e-01_rb,&
       & 9.370131e-01_rb,9.389529e-01_rb,9.406954e-01_rb,9.422727e-01_rb,9.437088e-01_rb,&
       & 9.450221e-01_rb,9.462308e-01_rb,9.473488e-01_rb,9.483830e-01_rb,9.493492e-01_rb,&
       & 9.502541e-01_rb,9.510999e-01_rb,9.518971e-01_rb,9.526455e-01_rb,9.533554e-01_rb,&
       & 9.540249e-01_rb,9.546571e-01_rb,9.552551e-01_rb,9.558258e-01_rb,9.563603e-01_rb,&
       & 9.568713e-01_rb,9.573569e-01_rb,9.578141e-01_rb,9.582485e-01_rb,9.586604e-01_rb,&
       & 9.590525e-01_rb,9.594218e-01_rb,9.597710e-01_rb,9.601052e-01_rb,9.604181e-01_rb,&
       & 9.607159e-01_rb,9.609979e-01_rb,9.612655e-01_rb,9.615184e-01_rb,9.617564e-01_rb,&
       & 9.619860e-01_rb,9.622009e-01_rb,9.624031e-01_rb,9.625957e-01_rb,9.627792e-01_rb,&
       & 9.629530e-01_rb,9.631171e-01_rb,9.632746e-01_rb /)
!     BAND  18
      asyliq1(:, 18) = (/ &
       & 8.574638e-01_rb,8.351383e-01_rb,8.142977e-01_rb,8.083068e-01_rb,8.129284e-01_rb,&
       & 8.215827e-01_rb,8.307238e-01_rb,8.389963e-01_rb,8.460481e-01_rb,8.519273e-01_rb,&
       & 8.568153e-01_rb,8.609116e-01_rb,8.643892e-01_rb,8.673941e-01_rb,8.700248e-01_rb,&
       & 8.723707e-01_rb,8.744902e-01_rb,8.764240e-01_rb,8.782057e-01_rb,8.798593e-01_rb,&
       & 8.814063e-01_rb,8.828573e-01_rb,8.842261e-01_rb,8.855196e-01_rb,8.867497e-01_rb,&
       & 8.879164e-01_rb,8.890316e-01_rb,8.900941e-01_rb,8.911118e-01_rb,8.920832e-01_rb,&
       & 8.930156e-01_rb,8.939091e-01_rb,8.947663e-01_rb,8.955888e-01_rb,8.963786e-01_rb,&
       & 8.971350e-01_rb,8.978617e-01_rb,8.985590e-01_rb,8.992243e-01_rb,8.998631e-01_rb,&
       & 9.004753e-01_rb,9.010602e-01_rb,9.016192e-01_rb,9.021542e-01_rb,9.026644e-01_rb,&
       & 9.031535e-01_rb,9.036194e-01_rb,9.040656e-01_rb,9.044894e-01_rb,9.048933e-01_rb,&
       & 9.052789e-01_rb,9.056481e-01_rb,9.060004e-01_rb,9.063343e-01_rb,9.066544e-01_rb,&
       & 9.069604e-01_rb,9.072512e-01_rb,9.075290e-01_rb /)
!     BAND  19
      asyliq1(:, 19) = (/ &
       & 8.349569e-01_rb,8.034579e-01_rb,7.932136e-01_rb,8.010156e-01_rb,8.137083e-01_rb,&
       & 8.255339e-01_rb,8.351938e-01_rb,8.428286e-01_rb,8.488944e-01_rb,8.538187e-01_rb,&
       & 8.579255e-01_rb,8.614473e-01_rb,8.645338e-01_rb,8.672908e-01_rb,8.697947e-01_rb,&
       & 8.720843e-01_rb,8.742015e-01_rb,8.761718e-01_rb,8.780160e-01_rb,8.797479e-01_rb,&
       & 8.813810e-01_rb,8.829250e-01_rb,8.843907e-01_rb,8.857822e-01_rb,8.871059e-01_rb,&
       & 8.883724e-01_rb,8.895810e-01_rb,8.907384e-01_rb,8.918456e-01_rb,8.929083e-01_rb,&
       & 8.939284e-01_rb,8.949060e-01_rb,8.958463e-01_rb,8.967486e-01_rb,8.976129e-01_rb,&
       & 8.984463e-01_rb,8.992439e-01_rb,9.000094e-01_rb,9.007438e-01_rb,9.014496e-01_rb,&
       & 9.021235e-01_rb,9.027699e-01_rb,9.033859e-01_rb,9.039772e-01_rb,9.045419e-01_rb,&
       & 9.050819e-01_rb,9.055975e-01_rb,9.060907e-01_rb,9.065607e-01_rb,9.070093e-01_rb,&
       & 9.074389e-01_rb,9.078475e-01_rb,9.082388e-01_rb,9.086117e-01_rb,9.089678e-01_rb,&
       & 9.093081e-01_rb,9.096307e-01_rb,9.099410e-01_rb /)
!     BAND  20
      asyliq1(:, 20) = (/ &
       & 8.109692e-01_rb,7.846657e-01_rb,7.881928e-01_rb,8.009509e-01_rb,8.131208e-01_rb,&
       & 8.230400e-01_rb,8.309448e-01_rb,8.372920e-01_rb,8.424837e-01_rb,8.468166e-01_rb,&
       & 8.504947e-01_rb,8.536642e-01_rb,8.564256e-01_rb,8.588513e-01_rb,8.610011e-01_rb,&
       & 8.629122e-01_rb,8.646262e-01_rb,8.661720e-01_rb,8.675752e-01_rb,8.688582e-01_rb,&
       & 8.700379e-01_rb,8.711300e-01_rb,8.721485e-01_rb,8.731027e-01_rb,8.740010e-01_rb,&
       & 8.748499e-01_rb,8.756564e-01_rb,8.764239e-01_rb,8.771542e-01_rb,8.778523e-01_rb,&
       & 8.785211e-01_rb,8.791601e-01_rb,8.797725e-01_rb,8.803589e-01_rb,8.809173e-01_rb,&
       & 8.814552e-01_rb,8.819705e-01_rb,8.824611e-01_rb,8.829311e-01_rb,8.833791e-01_rb,&
       & 8.838078e-01_rb,8.842148e-01_rb,8.846044e-01_rb,8.849756e-01_rb,8.853291e-01_rb,&
       & 8.856645e-01_rb,8.859841e-01_rb,8.862904e-01_rb,8.865801e-01_rb,8.868551e-01_rb,&
       & 8.871182e-01_rb,8.873673e-01_rb,8.876059e-01_rb,8.878307e-01_rb,8.880462e-01_rb,&
       & 8.882501e-01_rb,8.884453e-01_rb,8.886339e-01_rb /)
!     BAND  21
      asyliq1(:, 21) = (/ &
       & 7.838510e-01_rb,7.803151e-01_rb,7.980477e-01_rb,8.144160e-01_rb,8.261784e-01_rb,&
       & 8.344240e-01_rb,8.404278e-01_rb,8.450391e-01_rb,8.487593e-01_rb,8.518741e-01_rb,&
       & 8.545484e-01_rb,8.568890e-01_rb,8.589560e-01_rb,8.607983e-01_rb,8.624504e-01_rb,&
       & 8.639408e-01_rb,8.652945e-01_rb,8.665301e-01_rb,8.676634e-01_rb,8.687121e-01_rb,&
       & 8.696855e-01_rb,8.705933e-01_rb,8.714448e-01_rb,8.722454e-01_rb,8.730014e-01_rb,&
       & 8.737180e-01_rb,8.743982e-01_rb,8.750436e-01_rb,8.756598e-01_rb,8.762481e-01_rb,&
       & 8.768089e-01_rb,8.773427e-01_rb,8.778532e-01_rb,8.783434e-01_rb,8.788089e-01_rb,&
       & 8.792530e-01_rb,8.796784e-01_rb,8.800845e-01_rb,8.804716e-01_rb,8.808411e-01_rb,&
       & 8.811923e-01_rb,8.815276e-01_rb,8.818472e-01_rb,8.821504e-01_rb,8.824408e-01_rb,&
       & 8.827155e-01_rb,8.829777e-01_rb,8.832269e-01_rb,8.834631e-01_rb,8.836892e-01_rb,&
       & 8.839034e-01_rb,8.841075e-01_rb,8.843021e-01_rb,8.844866e-01_rb,8.846631e-01_rb,&
       & 8.848304e-01_rb,8.849910e-01_rb,8.851425e-01_rb /)
!     BAND  22
      asyliq1(:, 22) = (/ &
       & 7.760783e-01_rb,7.890215e-01_rb,8.090192e-01_rb,8.230252e-01_rb,8.321369e-01_rb,&
       & 8.384258e-01_rb,8.431529e-01_rb,8.469558e-01_rb,8.501499e-01_rb,8.528899e-01_rb,&
       & 8.552899e-01_rb,8.573956e-01_rb,8.592570e-01_rb,8.609098e-01_rb,8.623897e-01_rb,&
       & 8.637169e-01_rb,8.649184e-01_rb,8.660097e-01_rb,8.670096e-01_rb,8.679338e-01_rb,&
       & 8.687896e-01_rb,8.695880e-01_rb,8.703365e-01_rb,8.710422e-01_rb,8.717092e-01_rb,&
       & 8.723378e-01_rb,8.729363e-01_rb,8.735063e-01_rb,8.740475e-01_rb,8.745661e-01_rb,&
       & 8.750560e-01_rb,8.755275e-01_rb,8.759731e-01_rb,8.764000e-01_rb,8.768071e-01_rb,&
       & 8.771942e-01_rb,8.775628e-01_rb,8.779126e-01_rb,8.782483e-01_rb,8.785626e-01_rb,&
       & 8.788610e-01_rb,8.791482e-01_rb,8.794180e-01_rb,8.796765e-01_rb,8.799207e-01_rb,&
       & 8.801522e-01_rb,8.803707e-01_rb,8.805777e-01_rb,8.807749e-01_rb,8.809605e-01_rb,&
       & 8.811362e-01_rb,8.813047e-01_rb,8.814647e-01_rb,8.816131e-01_rb,8.817588e-01_rb,&
       & 8.818930e-01_rb,8.820230e-01_rb,8.821445e-01_rb /)
!     BAND  23
      asyliq1(:, 23) = (/ &
       & 7.847907e-01_rb,8.099917e-01_rb,8.257428e-01_rb,8.350423e-01_rb,8.411971e-01_rb,&
       & 8.457241e-01_rb,8.493010e-01_rb,8.522565e-01_rb,8.547660e-01_rb,8.569311e-01_rb,&
       & 8.588181e-01_rb,8.604729e-01_rb,8.619296e-01_rb,8.632208e-01_rb,8.643725e-01_rb,&
       & 8.654050e-01_rb,8.663363e-01_rb,8.671835e-01_rb,8.679590e-01_rb,8.686707e-01_rb,&
       & 8.693308e-01_rb,8.699433e-01_rb,8.705147e-01_rb,8.710490e-01_rb,8.715497e-01_rb,&
       & 8.720219e-01_rb,8.724669e-01_rb,8.728849e-01_rb,8.732806e-01_rb,8.736550e-01_rb,&
       & 8.740099e-01_rb,8.743435e-01_rb,8.746601e-01_rb,8.749610e-01_rb,8.752449e-01_rb,&
       & 8.755143e-01_rb,8.757688e-01_rb,8.760095e-01_rb,8.762375e-01_rb,8.764532e-01_rb,&
       & 8.766579e-01_rb,8.768506e-01_rb,8.770323e-01_rb,8.772049e-01_rb,8.773690e-01_rb,&
       & 8.775226e-01_rb,8.776679e-01_rb,8.778062e-01_rb,8.779360e-01_rb,8.780587e-01_rb,&
       & 8.781747e-01_rb,8.782852e-01_rb,8.783892e-01_rb,8.784891e-01_rb,8.785824e-01_rb,&
       & 8.786705e-01_rb,8.787546e-01_rb,8.788336e-01_rb /)
!     BAND  24
      asyliq1(:, 24) = (/ &
       & 8.054324e-01_rb,8.266282e-01_rb,8.378075e-01_rb,8.449848e-01_rb,8.502166e-01_rb,&
       & 8.542268e-01_rb,8.573477e-01_rb,8.598022e-01_rb,8.617689e-01_rb,8.633859e-01_rb,&
       & 8.647536e-01_rb,8.659354e-01_rb,8.669807e-01_rb,8.679143e-01_rb,8.687577e-01_rb,&
       & 8.695222e-01_rb,8.702207e-01_rb,8.708591e-01_rb,8.714446e-01_rb,8.719836e-01_rb,&
       & 8.724812e-01_rb,8.729426e-01_rb,8.733689e-01_rb,8.737665e-01_rb,8.741373e-01_rb,&
       & 8.744834e-01_rb,8.748070e-01_rb,8.751131e-01_rb,8.754011e-01_rb,8.756676e-01_rb,&
       & 8.759219e-01_rb,8.761599e-01_rb,8.763857e-01_rb,8.765984e-01_rb,8.767999e-01_rb,&
       & 8.769889e-01_rb,8.771669e-01_rb,8.773373e-01_rb,8.774969e-01_rb,8.776469e-01_rb,&
       & 8.777894e-01_rb,8.779237e-01_rb,8.780505e-01_rb,8.781703e-01_rb,8.782820e-01_rb,&
       & 8.783886e-01_rb,8.784894e-01_rb,8.785844e-01_rb,8.786736e-01_rb,8.787584e-01_rb,&
       & 8.788379e-01_rb,8.789130e-01_rb,8.789849e-01_rb,8.790506e-01_rb,8.791141e-01_rb,&
       & 8.791750e-01_rb,8.792324e-01_rb,8.792867e-01_rb /)
!     BAND  25
      asyliq1(:, 25) = (/ &
       & 8.249534e-01_rb,8.391988e-01_rb,8.474107e-01_rb,8.526860e-01_rb,8.563983e-01_rb,&
       & 8.592389e-01_rb,8.615144e-01_rb,8.633790e-01_rb,8.649325e-01_rb,8.662504e-01_rb,&
       & 8.673841e-01_rb,8.683741e-01_rb,8.692495e-01_rb,8.700309e-01_rb,8.707328e-01_rb,&
       & 8.713650e-01_rb,8.719432e-01_rb,8.724676e-01_rb,8.729498e-01_rb,8.733922e-01_rb,&
       & 8.737981e-01_rb,8.741745e-01_rb,8.745225e-01_rb,8.748467e-01_rb,8.751512e-01_rb,&
       & 8.754315e-01_rb,8.756962e-01_rb,8.759450e-01_rb,8.761774e-01_rb,8.763945e-01_rb,&
       & 8.766021e-01_rb,8.767970e-01_rb,8.769803e-01_rb,8.771511e-01_rb,8.773151e-01_rb,&
       & 8.774689e-01_rb,8.776147e-01_rb,8.777533e-01_rb,8.778831e-01_rb,8.780050e-01_rb,&
       & 8.781197e-01_rb,8.782301e-01_rb,8.783323e-01_rb,8.784312e-01_rb,8.785222e-01_rb,&
       & 8.786096e-01_rb,8.786916e-01_rb,8.787688e-01_rb,8.788411e-01_rb,8.789122e-01_rb,&
       & 8.789762e-01_rb,8.790373e-01_rb,8.790954e-01_rb,8.791514e-01_rb,8.792018e-01_rb,&
       & 8.792517e-01_rb,8.792990e-01_rb,8.793429e-01_rb /)
!     BAND  26
      asyliq1(:, 26) = (/ &
       & 8.323091e-01_rb,8.429776e-01_rb,8.498123e-01_rb,8.546929e-01_rb,8.584295e-01_rb,&
       & 8.613489e-01_rb,8.636324e-01_rb,8.654303e-01_rb,8.668675e-01_rb,8.680404e-01_rb,&
       & 8.690174e-01_rb,8.698495e-01_rb,8.705666e-01_rb,8.711961e-01_rb,8.717556e-01_rb,&
       & 8.722546e-01_rb,8.727063e-01_rb,8.731170e-01_rb,8.734933e-01_rb,8.738382e-01_rb,&
       & 8.741590e-01_rb,8.744525e-01_rb,8.747295e-01_rb,8.749843e-01_rb,8.752210e-01_rb,&
       & 8.754437e-01_rb,8.756524e-01_rb,8.758472e-01_rb,8.760288e-01_rb,8.762030e-01_rb,&
       & 8.763603e-01_rb,8.765122e-01_rb,8.766539e-01_rb,8.767894e-01_rb,8.769130e-01_rb,&
       & 8.770310e-01_rb,8.771422e-01_rb,8.772437e-01_rb,8.773419e-01_rb,8.774355e-01_rb,&
       & 8.775221e-01_rb,8.776047e-01_rb,8.776802e-01_rb,8.777539e-01_rb,8.778216e-01_rb,&
       & 8.778859e-01_rb,8.779473e-01_rb,8.780031e-01_rb,8.780562e-01_rb,8.781097e-01_rb,&
       & 8.781570e-01_rb,8.782021e-01_rb,8.782463e-01_rb,8.782845e-01_rb,8.783235e-01_rb,&
       & 8.783610e-01_rb,8.783953e-01_rb,8.784273e-01_rb /)
!     BAND  27
      asyliq1(:, 27) = (/ &
       & 8.396448e-01_rb,8.480172e-01_rb,8.535934e-01_rb,8.574145e-01_rb,8.600835e-01_rb,&
       & 8.620347e-01_rb,8.635500e-01_rb,8.648003e-01_rb,8.658758e-01_rb,8.668248e-01_rb,&
       & 8.676697e-01_rb,8.684220e-01_rb,8.690893e-01_rb,8.696807e-01_rb,8.702046e-01_rb,&
       & 8.706676e-01_rb,8.710798e-01_rb,8.714478e-01_rb,8.717778e-01_rb,8.720747e-01_rb,&
       & 8.723431e-01_rb,8.725889e-01_rb,8.728144e-01_rb,8.730201e-01_rb,8.732129e-01_rb,&
       & 8.733907e-01_rb,8.735541e-01_rb,8.737100e-01_rb,8.738533e-01_rb,8.739882e-01_rb,&
       & 8.741164e-01_rb,8.742362e-01_rb,8.743485e-01_rb,8.744530e-01_rb,8.745512e-01_rb,&
       & 8.746471e-01_rb,8.747373e-01_rb,8.748186e-01_rb,8.748973e-01_rb,8.749732e-01_rb,&
       & 8.750443e-01_rb,8.751105e-01_rb,8.751747e-01_rb,8.752344e-01_rb,8.752902e-01_rb,&
       & 8.753412e-01_rb,8.753917e-01_rb,8.754393e-01_rb,8.754843e-01_rb,8.755282e-01_rb,&
       & 8.755662e-01_rb,8.756039e-01_rb,8.756408e-01_rb,8.756722e-01_rb,8.757072e-01_rb,&
       & 8.757352e-01_rb,8.757653e-01_rb,8.757932e-01_rb /)
!     BAND  28
      asyliq1(:, 28) = (/ &
       & 8.374590e-01_rb,8.465669e-01_rb,8.518701e-01_rb,8.547627e-01_rb,8.565745e-01_rb,&
       & 8.579065e-01_rb,8.589717e-01_rb,8.598632e-01_rb,8.606363e-01_rb,8.613268e-01_rb,&
       & 8.619560e-01_rb,8.625340e-01_rb,8.630689e-01_rb,8.635601e-01_rb,8.640084e-01_rb,&
       & 8.644180e-01_rb,8.647885e-01_rb,8.651220e-01_rb,8.654218e-01_rb,8.656908e-01_rb,&
       & 8.659294e-01_rb,8.661422e-01_rb,8.663334e-01_rb,8.665037e-01_rb,8.666543e-01_rb,&
       & 8.667913e-01_rb,8.669156e-01_rb,8.670242e-01_rb,8.671249e-01_rb,8.672161e-01_rb,&
       & 8.672993e-01_rb,8.673733e-01_rb,8.674457e-01_rb,8.675103e-01_rb,8.675713e-01_rb,&
       & 8.676267e-01_rb,8.676798e-01_rb,8.677286e-01_rb,8.677745e-01_rb,8.678178e-01_rb,&
       & 8.678601e-01_rb,8.678986e-01_rb,8.679351e-01_rb,8.679693e-01_rb,8.680013e-01_rb,&
       & 8.680334e-01_rb,8.680624e-01_rb,8.680915e-01_rb,8.681178e-01_rb,8.681428e-01_rb,&
       & 8.681654e-01_rb,8.681899e-01_rb,8.682103e-01_rb,8.682317e-01_rb,8.682498e-01_rb,&
       & 8.682677e-01_rb,8.682861e-01_rb,8.683041e-01_rb /)
!     BAND  29
      asyliq1(:, 29) = (/ &
       & 7.877069e-01_rb,8.244281e-01_rb,8.367971e-01_rb,8.409074e-01_rb,8.429859e-01_rb,&
       & 8.454386e-01_rb,8.489350e-01_rb,8.534141e-01_rb,8.585814e-01_rb,8.641267e-01_rb,&
       & 8.697999e-01_rb,8.754223e-01_rb,8.808785e-01_rb,8.860944e-01_rb,8.910354e-01_rb,&
       & 8.956837e-01_rb,9.000392e-01_rb,9.041091e-01_rb,9.079071e-01_rb,9.114479e-01_rb,&
       & 9.147462e-01_rb,9.178234e-01_rb,9.206903e-01_rb,9.233663e-01_rb,9.258668e-01_rb,&
       & 9.282006e-01_rb,9.303847e-01_rb,9.324288e-01_rb,9.343418e-01_rb,9.361356e-01_rb,&
       & 9.378176e-01_rb,9.393939e-01_rb,9.408736e-01_rb,9.422622e-01_rb,9.435670e-01_rb,&
       & 9.447900e-01_rb,9.459395e-01_rb,9.470199e-01_rb,9.480335e-01_rb,9.489852e-01_rb,&
       & 9.498782e-01_rb,9.507168e-01_rb,9.515044e-01_rb,9.522470e-01_rb,9.529409e-01_rb,&
       & 9.535946e-01_rb,9.542071e-01_rb,9.547838e-01_rb,9.553256e-01_rb,9.558351e-01_rb,&
       & 9.563139e-01_rb,9.567660e-01_rb,9.571915e-01_rb,9.575901e-01_rb,9.579685e-01_rb,&
       & 9.583239e-01_rb,9.586602e-01_rb,9.589766e-01_rb /)


! Spherical Ice Particle Parameterization
! extinction units (ext coef/iwc): [(m^-1)/(g m^-3)]
      extice2(:, 16) = (/ &
! band 16
        & 4.101824e-01_rb,2.435514e-01_rb,1.713697e-01_rb,1.314865e-01_rb,1.063406e-01_rb,&
        & 8.910701e-02_rb,7.659480e-02_rb,6.711784e-02_rb,5.970353e-02_rb,5.375249e-02_rb,&
        & 4.887577e-02_rb,4.481025e-02_rb,4.137171e-02_rb,3.842744e-02_rb,3.587948e-02_rb,&
        & 3.365396e-02_rb,3.169419e-02_rb,2.995593e-02_rb,2.840419e-02_rb,2.701091e-02_rb,&
        & 2.575336e-02_rb,2.461293e-02_rb,2.357423e-02_rb,2.262443e-02_rb,2.175276e-02_rb,&
        & 2.095012e-02_rb,2.020875e-02_rb,1.952199e-02_rb,1.888412e-02_rb,1.829018e-02_rb,&
        & 1.773586e-02_rb,1.721738e-02_rb,1.673144e-02_rb,1.627510e-02_rb,1.584579e-02_rb,&
        & 1.544122e-02_rb,1.505934e-02_rb,1.469833e-02_rb,1.435654e-02_rb,1.403251e-02_rb,&
        & 1.372492e-02_rb,1.343255e-02_rb,1.315433e-02_rb /)
      extice2(:, 17) = (/ &
! band 17
        & 3.836650e-01_rb,2.304055e-01_rb,1.637265e-01_rb,1.266681e-01_rb,1.031602e-01_rb,&
        & 8.695191e-02_rb,7.511544e-02_rb,6.610009e-02_rb,5.900909e-02_rb,5.328833e-02_rb,&
        & 4.857728e-02_rb,4.463133e-02_rb,4.127880e-02_rb,3.839567e-02_rb,3.589013e-02_rb,&
        & 3.369280e-02_rb,3.175027e-02_rb,3.002079e-02_rb,2.847121e-02_rb,2.707493e-02_rb,&
        & 2.581031e-02_rb,2.465962e-02_rb,2.360815e-02_rb,2.264363e-02_rb,2.175571e-02_rb,&
        & 2.093563e-02_rb,2.017592e-02_rb,1.947015e-02_rb,1.881278e-02_rb,1.819901e-02_rb,&
        & 1.762463e-02_rb,1.708598e-02_rb,1.657982e-02_rb,1.610330e-02_rb,1.565390e-02_rb,&
        & 1.522937e-02_rb,1.482768e-02_rb,1.444706e-02_rb,1.408588e-02_rb,1.374270e-02_rb,&
        & 1.341619e-02_rb,1.310517e-02_rb,1.280857e-02_rb /)
      extice2(:, 18) = (/ &
! band 18
        & 4.152673e-01_rb,2.436816e-01_rb,1.702243e-01_rb,1.299704e-01_rb,1.047528e-01_rb,&
        & 8.756039e-02_rb,7.513327e-02_rb,6.575690e-02_rb,5.844616e-02_rb,5.259609e-02_rb,&
        & 4.781531e-02_rb,4.383980e-02_rb,4.048517e-02_rb,3.761891e-02_rb,3.514342e-02_rb,&
        & 3.298525e-02_rb,3.108814e-02_rb,2.940825e-02_rb,2.791096e-02_rb,2.656858e-02_rb,&
        & 2.535869e-02_rb,2.426297e-02_rb,2.326627e-02_rb,2.235602e-02_rb,2.152164e-02_rb,&
        & 2.075420e-02_rb,2.004613e-02_rb,1.939091e-02_rb,1.878296e-02_rb,1.821744e-02_rb,&
        & 1.769015e-02_rb,1.719741e-02_rb,1.673600e-02_rb,1.630308e-02_rb,1.589615e-02_rb,&
        & 1.551298e-02_rb,1.515159e-02_rb,1.481021e-02_rb,1.448726e-02_rb,1.418131e-02_rb,&
        & 1.389109e-02_rb,1.361544e-02_rb,1.335330e-02_rb /)
      extice2(:, 19) = (/ &
! band 19
        & 3.873250e-01_rb,2.331609e-01_rb,1.655002e-01_rb,1.277753e-01_rb,1.038247e-01_rb,&
        & 8.731780e-02_rb,7.527638e-02_rb,6.611873e-02_rb,5.892850e-02_rb,5.313885e-02_rb,&
        & 4.838068e-02_rb,4.440356e-02_rb,4.103167e-02_rb,3.813804e-02_rb,3.562870e-02_rb,&
        & 3.343269e-02_rb,3.149539e-02_rb,2.977414e-02_rb,2.823510e-02_rb,2.685112e-02_rb,&
        & 2.560015e-02_rb,2.446411e-02_rb,2.342805e-02_rb,2.247948e-02_rb,2.160789e-02_rb,&
        & 2.080438e-02_rb,2.006139e-02_rb,1.937238e-02_rb,1.873177e-02_rb,1.813469e-02_rb,&
        & 1.757689e-02_rb,1.705468e-02_rb,1.656479e-02_rb,1.610435e-02_rb,1.567081e-02_rb,&
        & 1.526192e-02_rb,1.487565e-02_rb,1.451020e-02_rb,1.416396e-02_rb,1.383546e-02_rb,&
        & 1.352339e-02_rb,1.322657e-02_rb,1.294392e-02_rb /)
      extice2(:, 20) = (/ &
! band 20
        & 3.784280e-01_rb,2.291396e-01_rb,1.632551e-01_rb,1.263775e-01_rb,1.028944e-01_rb,&
        & 8.666975e-02_rb,7.480952e-02_rb,6.577335e-02_rb,5.866714e-02_rb,5.293694e-02_rb,&
        & 4.822153e-02_rb,4.427547e-02_rb,4.092626e-02_rb,3.804918e-02_rb,3.555184e-02_rb,&
        & 3.336440e-02_rb,3.143307e-02_rb,2.971577e-02_rb,2.817912e-02_rb,2.679632e-02_rb,&
        & 2.554558e-02_rb,2.440903e-02_rb,2.337187e-02_rb,2.242173e-02_rb,2.154821e-02_rb,&
        & 2.074249e-02_rb,1.999706e-02_rb,1.930546e-02_rb,1.866212e-02_rb,1.806221e-02_rb,&
        & 1.750152e-02_rb,1.697637e-02_rb,1.648352e-02_rb,1.602010e-02_rb,1.558358e-02_rb,&
        & 1.517172e-02_rb,1.478250e-02_rb,1.441413e-02_rb,1.406498e-02_rb,1.373362e-02_rb,&
        & 1.341872e-02_rb,1.311911e-02_rb,1.283371e-02_rb /)
      extice2(:, 21) = (/ &
! band 21
        & 3.719909e-01_rb,2.259490e-01_rb,1.613144e-01_rb,1.250648e-01_rb,1.019462e-01_rb,&
        & 8.595358e-02_rb,7.425064e-02_rb,6.532618e-02_rb,5.830218e-02_rb,5.263421e-02_rb,&
        & 4.796697e-02_rb,4.405891e-02_rb,4.074013e-02_rb,3.788776e-02_rb,3.541071e-02_rb,&
        & 3.324008e-02_rb,3.132280e-02_rb,2.961733e-02_rb,2.809071e-02_rb,2.671645e-02_rb,&
        & 2.547302e-02_rb,2.434276e-02_rb,2.331102e-02_rb,2.236558e-02_rb,2.149614e-02_rb,&
        & 2.069397e-02_rb,1.995163e-02_rb,1.926272e-02_rb,1.862174e-02_rb,1.802389e-02_rb,&
        & 1.746500e-02_rb,1.694142e-02_rb,1.644994e-02_rb,1.598772e-02_rb,1.555225e-02_rb,&
        & 1.514129e-02_rb,1.475286e-02_rb,1.438515e-02_rb,1.403659e-02_rb,1.370572e-02_rb,&
        & 1.339124e-02_rb,1.309197e-02_rb,1.280685e-02_rb /)
      extice2(:, 22) = (/ &
! band 22
        & 3.713158e-01_rb,2.253816e-01_rb,1.608461e-01_rb,1.246718e-01_rb,1.016109e-01_rb,&
        & 8.566332e-02_rb,7.399666e-02_rb,6.510199e-02_rb,5.810290e-02_rb,5.245608e-02_rb,&
        & 4.780702e-02_rb,4.391478e-02_rb,4.060989e-02_rb,3.776982e-02_rb,3.530374e-02_rb,&
        & 3.314296e-02_rb,3.123458e-02_rb,2.953719e-02_rb,2.801794e-02_rb,2.665043e-02_rb,&
        & 2.541321e-02_rb,2.428868e-02_rb,2.326224e-02_rb,2.232173e-02_rb,2.145688e-02_rb,&
        & 2.065899e-02_rb,1.992067e-02_rb,1.923552e-02_rb,1.859808e-02_rb,1.800356e-02_rb,&
        & 1.744782e-02_rb,1.692721e-02_rb,1.643855e-02_rb,1.597900e-02_rb,1.554606e-02_rb,&
        & 1.513751e-02_rb,1.475137e-02_rb,1.438586e-02_rb,1.403938e-02_rb,1.371050e-02_rb,&
        & 1.339793e-02_rb,1.310050e-02_rb,1.281713e-02_rb /)
      extice2(:, 23) = (/ &
! band 23
        & 3.605883e-01_rb,2.204388e-01_rb,1.580431e-01_rb,1.229033e-01_rb,1.004203e-01_rb,&
        & 8.482616e-02_rb,7.338941e-02_rb,6.465105e-02_rb,5.776176e-02_rb,5.219398e-02_rb,&
        & 4.760288e-02_rb,4.375369e-02_rb,4.048111e-02_rb,3.766539e-02_rb,3.521771e-02_rb,&
        & 3.307079e-02_rb,3.117277e-02_rb,2.948303e-02_rb,2.796929e-02_rb,2.660560e-02_rb,&
        & 2.537086e-02_rb,2.424772e-02_rb,2.322182e-02_rb,2.228114e-02_rb,2.141556e-02_rb,&
        & 2.061649e-02_rb,1.987661e-02_rb,1.918962e-02_rb,1.855009e-02_rb,1.795330e-02_rb,&
        & 1.739514e-02_rb,1.687199e-02_rb,1.638069e-02_rb,1.591845e-02_rb,1.548276e-02_rb,&
        & 1.507143e-02_rb,1.468249e-02_rb,1.431416e-02_rb,1.396486e-02_rb,1.363318e-02_rb,&
        & 1.331781e-02_rb,1.301759e-02_rb,1.273147e-02_rb /)
      extice2(:, 24) = (/ &
! band 24
        & 3.527890e-01_rb,2.168469e-01_rb,1.560090e-01_rb,1.216216e-01_rb,9.955787e-02_rb,&
        & 8.421942e-02_rb,7.294827e-02_rb,6.432192e-02_rb,5.751081e-02_rb,5.199888e-02_rb,&
        & 4.744835e-02_rb,4.362899e-02_rb,4.037847e-02_rb,3.757910e-02_rb,3.514351e-02_rb,&
        & 3.300546e-02_rb,3.111382e-02_rb,2.942853e-02_rb,2.791775e-02_rb,2.655584e-02_rb,&
        & 2.532195e-02_rb,2.419892e-02_rb,2.317255e-02_rb,2.223092e-02_rb,2.136402e-02_rb,&
        & 2.056334e-02_rb,1.982160e-02_rb,1.913258e-02_rb,1.849087e-02_rb,1.789178e-02_rb,&
        & 1.733124e-02_rb,1.680565e-02_rb,1.631187e-02_rb,1.584711e-02_rb,1.540889e-02_rb,&
        & 1.499502e-02_rb,1.460354e-02_rb,1.423269e-02_rb,1.388088e-02_rb,1.354670e-02_rb,&
        & 1.322887e-02_rb,1.292620e-02_rb,1.263767e-02_rb /)
      extice2(:, 25) = (/ &
! band 25
        & 3.477874e-01_rb,2.143515e-01_rb,1.544887e-01_rb,1.205942e-01_rb,9.881779e-02_rb,&
        & 8.366261e-02_rb,7.251586e-02_rb,6.397790e-02_rb,5.723183e-02_rb,5.176908e-02_rb,&
        & 4.725658e-02_rb,4.346715e-02_rb,4.024055e-02_rb,3.746055e-02_rb,3.504080e-02_rb,&
        & 3.291583e-02_rb,3.103507e-02_rb,2.935891e-02_rb,2.785582e-02_rb,2.650042e-02_rb,&
        & 2.527206e-02_rb,2.415376e-02_rb,2.313142e-02_rb,2.219326e-02_rb,2.132934e-02_rb,&
        & 2.053122e-02_rb,1.979169e-02_rb,1.910456e-02_rb,1.846448e-02_rb,1.786680e-02_rb,&
        & 1.730745e-02_rb,1.678289e-02_rb,1.628998e-02_rb,1.582595e-02_rb,1.538835e-02_rb,&
        & 1.497499e-02_rb,1.458393e-02_rb,1.421341e-02_rb,1.386187e-02_rb,1.352788e-02_rb,&
        & 1.321019e-02_rb,1.290762e-02_rb,1.261913e-02_rb /)
      extice2(:, 26) = (/ &
! band 26
        & 3.453721e-01_rb,2.130744e-01_rb,1.536698e-01_rb,1.200140e-01_rb,9.838078e-02_rb,&
        & 8.331940e-02_rb,7.223803e-02_rb,6.374775e-02_rb,5.703770e-02_rb,5.160290e-02_rb,&
        & 4.711259e-02_rb,4.334110e-02_rb,4.012923e-02_rb,3.736150e-02_rb,3.495208e-02_rb,&
        & 3.283589e-02_rb,3.096267e-02_rb,2.929302e-02_rb,2.779560e-02_rb,2.644517e-02_rb,&
        & 2.522119e-02_rb,2.410677e-02_rb,2.308788e-02_rb,2.215281e-02_rb,2.129165e-02_rb,&
        & 2.049602e-02_rb,1.975874e-02_rb,1.907365e-02_rb,1.843542e-02_rb,1.783943e-02_rb,&
        & 1.728162e-02_rb,1.675847e-02_rb,1.626685e-02_rb,1.580401e-02_rb,1.536750e-02_rb,&
        & 1.495515e-02_rb,1.456502e-02_rb,1.419537e-02_rb,1.384463e-02_rb,1.351139e-02_rb,&
        & 1.319438e-02_rb,1.289246e-02_rb,1.260456e-02_rb /)
      extice2(:, 27) = (/ &
! band 27
        & 3.417883e-01_rb,2.113379e-01_rb,1.526395e-01_rb,1.193347e-01_rb,9.790253e-02_rb,&
        & 8.296715e-02_rb,7.196979e-02_rb,6.353806e-02_rb,5.687024e-02_rb,5.146670e-02_rb,&
        & 4.700001e-02_rb,4.324667e-02_rb,4.004894e-02_rb,3.729233e-02_rb,3.489172e-02_rb,&
        & 3.278257e-02_rb,3.091499e-02_rb,2.924987e-02_rb,2.775609e-02_rb,2.640859e-02_rb,&
        & 2.518695e-02_rb,2.407439e-02_rb,2.305697e-02_rb,2.212303e-02_rb,2.126273e-02_rb,&
        & 2.046774e-02_rb,1.973090e-02_rb,1.904610e-02_rb,1.840801e-02_rb,1.781204e-02_rb,&
        & 1.725417e-02_rb,1.673086e-02_rb,1.623902e-02_rb,1.577590e-02_rb,1.533906e-02_rb,&
        & 1.492634e-02_rb,1.453580e-02_rb,1.416571e-02_rb,1.381450e-02_rb,1.348078e-02_rb,&
        & 1.316327e-02_rb,1.286082e-02_rb,1.257240e-02_rb /)
      extice2(:, 28) = (/ &
! band 28
        & 3.416111e-01_rb,2.114124e-01_rb,1.527734e-01_rb,1.194809e-01_rb,9.804612e-02_rb,&
        & 8.310287e-02_rb,7.209595e-02_rb,6.365442e-02_rb,5.697710e-02_rb,5.156460e-02_rb,&
        & 4.708957e-02_rb,4.332850e-02_rb,4.012361e-02_rb,3.736037e-02_rb,3.495364e-02_rb,&
        & 3.283879e-02_rb,3.096593e-02_rb,2.929589e-02_rb,2.779751e-02_rb,2.644571e-02_rb,&
        & 2.522004e-02_rb,2.410369e-02_rb,2.308271e-02_rb,2.214542e-02_rb,2.128195e-02_rb,&
        & 2.048396e-02_rb,1.974429e-02_rb,1.905679e-02_rb,1.841614e-02_rb,1.781774e-02_rb,&
        & 1.725754e-02_rb,1.673203e-02_rb,1.623807e-02_rb,1.577293e-02_rb,1.533416e-02_rb,&
        & 1.491958e-02_rb,1.452727e-02_rb,1.415547e-02_rb,1.380262e-02_rb,1.346732e-02_rb,&
        & 1.314830e-02_rb,1.284439e-02_rb,1.255456e-02_rb /)
      extice2(:, 29) = (/ &
! band 29
        & 4.196611e-01_rb,2.493642e-01_rb,1.761261e-01_rb,1.357197e-01_rb,1.102161e-01_rb,&
        & 9.269376e-02_rb,7.992985e-02_rb,7.022538e-02_rb,6.260168e-02_rb,5.645603e-02_rb,&
        & 5.139732e-02_rb,4.716088e-02_rb,4.356133e-02_rb,4.046498e-02_rb,3.777303e-02_rb,&
        & 3.541094e-02_rb,3.332137e-02_rb,3.145954e-02_rb,2.978998e-02_rb,2.828419e-02_rb,&
        & 2.691905e-02_rb,2.567559e-02_rb,2.453811e-02_rb,2.349350e-02_rb,2.253072e-02_rb,&
        & 2.164042e-02_rb,2.081464e-02_rb,2.004652e-02_rb,1.933015e-02_rb,1.866041e-02_rb,&
        & 1.803283e-02_rb,1.744348e-02_rb,1.688894e-02_rb,1.636616e-02_rb,1.587244e-02_rb,&
        & 1.540539e-02_rb,1.496287e-02_rb,1.454295e-02_rb,1.414392e-02_rb,1.376423e-02_rb,&
        & 1.340247e-02_rb,1.305739e-02_rb,1.272784e-02_rb /)

! single-scattering albedo: unitless
      ssaice2(:, 16) = (/ &
! band 16
        & 6.630615e-01_rb,6.451169e-01_rb,6.333696e-01_rb,6.246927e-01_rb,6.178420e-01_rb,&
        & 6.121976e-01_rb,6.074069e-01_rb,6.032505e-01_rb,5.995830e-01_rb,5.963030e-01_rb,&
        & 5.933372e-01_rb,5.906311e-01_rb,5.881427e-01_rb,5.858395e-01_rb,5.836955e-01_rb,&
        & 5.816896e-01_rb,5.798046e-01_rb,5.780264e-01_rb,5.763429e-01_rb,5.747441e-01_rb,&
        & 5.732213e-01_rb,5.717672e-01_rb,5.703754e-01_rb,5.690403e-01_rb,5.677571e-01_rb,&
        & 5.665215e-01_rb,5.653297e-01_rb,5.641782e-01_rb,5.630643e-01_rb,5.619850e-01_rb,&
        & 5.609381e-01_rb,5.599214e-01_rb,5.589328e-01_rb,5.579707e-01_rb,5.570333e-01_rb,&
        & 5.561193e-01_rb,5.552272e-01_rb,5.543558e-01_rb,5.535041e-01_rb,5.526708e-01_rb,&
        & 5.518551e-01_rb,5.510561e-01_rb,5.502729e-01_rb /)
      ssaice2(:, 17) = (/ &
! band 17
        & 7.689749e-01_rb,7.398171e-01_rb,7.205819e-01_rb,7.065690e-01_rb,6.956928e-01_rb,&
        & 6.868989e-01_rb,6.795813e-01_rb,6.733606e-01_rb,6.679838e-01_rb,6.632742e-01_rb,&
        & 6.591036e-01_rb,6.553766e-01_rb,6.520197e-01_rb,6.489757e-01_rb,6.461991e-01_rb,&
        & 6.436531e-01_rb,6.413075e-01_rb,6.391375e-01_rb,6.371221e-01_rb,6.352438e-01_rb,&
        & 6.334876e-01_rb,6.318406e-01_rb,6.302918e-01_rb,6.288315e-01_rb,6.274512e-01_rb,&
        & 6.261436e-01_rb,6.249022e-01_rb,6.237211e-01_rb,6.225953e-01_rb,6.215201e-01_rb,&
        & 6.204914e-01_rb,6.195055e-01_rb,6.185592e-01_rb,6.176492e-01_rb,6.167730e-01_rb,&
        & 6.159280e-01_rb,6.151120e-01_rb,6.143228e-01_rb,6.135587e-01_rb,6.128177e-01_rb,&
        & 6.120984e-01_rb,6.113993e-01_rb,6.107189e-01_rb /)
      ssaice2(:, 18) = (/ &
! band 18
        & 9.956167e-01_rb,9.814770e-01_rb,9.716104e-01_rb,9.639746e-01_rb,9.577179e-01_rb,&
        & 9.524010e-01_rb,9.477672e-01_rb,9.436527e-01_rb,9.399467e-01_rb,9.365708e-01_rb,&
        & 9.334672e-01_rb,9.305921e-01_rb,9.279118e-01_rb,9.253993e-01_rb,9.230330e-01_rb,&
        & 9.207954e-01_rb,9.186719e-01_rb,9.166501e-01_rb,9.147199e-01_rb,9.128722e-01_rb,&
        & 9.110997e-01_rb,9.093956e-01_rb,9.077544e-01_rb,9.061708e-01_rb,9.046406e-01_rb,&
        & 9.031598e-01_rb,9.017248e-01_rb,9.003326e-01_rb,8.989804e-01_rb,8.976655e-01_rb,&
        & 8.963857e-01_rb,8.951389e-01_rb,8.939233e-01_rb,8.927370e-01_rb,8.915785e-01_rb,&
        & 8.904464e-01_rb,8.893392e-01_rb,8.882559e-01_rb,8.871951e-01_rb,8.861559e-01_rb,&
        & 8.851373e-01_rb,8.841383e-01_rb,8.831581e-01_rb /)
      ssaice2(:, 19) = (/ &
! band 19
        & 9.723177e-01_rb,9.452119e-01_rb,9.267592e-01_rb,9.127393e-01_rb,9.014238e-01_rb,&
        & 8.919334e-01_rb,8.837584e-01_rb,8.765773e-01_rb,8.701736e-01_rb,8.643950e-01_rb,&
        & 8.591299e-01_rb,8.542942e-01_rb,8.498230e-01_rb,8.456651e-01_rb,8.417794e-01_rb,&
        & 8.381324e-01_rb,8.346964e-01_rb,8.314484e-01_rb,8.283687e-01_rb,8.254408e-01_rb,&
        & 8.226505e-01_rb,8.199854e-01_rb,8.174348e-01_rb,8.149891e-01_rb,8.126403e-01_rb,&
        & 8.103808e-01_rb,8.082041e-01_rb,8.061044e-01_rb,8.040765e-01_rb,8.021156e-01_rb,&
        & 8.002174e-01_rb,7.983781e-01_rb,7.965941e-01_rb,7.948622e-01_rb,7.931795e-01_rb,&
        & 7.915432e-01_rb,7.899508e-01_rb,7.884002e-01_rb,7.868891e-01_rb,7.854156e-01_rb,&
        & 7.839779e-01_rb,7.825742e-01_rb,7.812031e-01_rb /)
      ssaice2(:, 20) = (/ &
! band 20
        & 9.933294e-01_rb,9.860917e-01_rb,9.811564e-01_rb,9.774008e-01_rb,9.743652e-01_rb,&
        & 9.718155e-01_rb,9.696159e-01_rb,9.676810e-01_rb,9.659531e-01_rb,9.643915e-01_rb,&
        & 9.629667e-01_rb,9.616561e-01_rb,9.604426e-01_rb,9.593125e-01_rb,9.582548e-01_rb,&
        & 9.572607e-01_rb,9.563227e-01_rb,9.554347e-01_rb,9.545915e-01_rb,9.537888e-01_rb,&
        & 9.530226e-01_rb,9.522898e-01_rb,9.515874e-01_rb,9.509130e-01_rb,9.502643e-01_rb,&
        & 9.496394e-01_rb,9.490366e-01_rb,9.484542e-01_rb,9.478910e-01_rb,9.473456e-01_rb,&
        & 9.468169e-01_rb,9.463039e-01_rb,9.458056e-01_rb,9.453212e-01_rb,9.448499e-01_rb,&
        & 9.443910e-01_rb,9.439438e-01_rb,9.435077e-01_rb,9.430821e-01_rb,9.426666e-01_rb,&
        & 9.422607e-01_rb,9.418638e-01_rb,9.414756e-01_rb /)
      ssaice2(:, 21) = (/ &
! band 21
        & 9.900787e-01_rb,9.828880e-01_rb,9.779258e-01_rb,9.741173e-01_rb,9.710184e-01_rb,&
        & 9.684012e-01_rb,9.661332e-01_rb,9.641301e-01_rb,9.623352e-01_rb,9.607083e-01_rb,&
        & 9.592198e-01_rb,9.578474e-01_rb,9.565739e-01_rb,9.553856e-01_rb,9.542715e-01_rb,&
        & 9.532226e-01_rb,9.522314e-01_rb,9.512919e-01_rb,9.503986e-01_rb,9.495472e-01_rb,&
        & 9.487337e-01_rb,9.479549e-01_rb,9.472077e-01_rb,9.464897e-01_rb,9.457985e-01_rb,&
        & 9.451322e-01_rb,9.444890e-01_rb,9.438673e-01_rb,9.432656e-01_rb,9.426826e-01_rb,&
        & 9.421173e-01_rb,9.415684e-01_rb,9.410351e-01_rb,9.405164e-01_rb,9.400115e-01_rb,&
        & 9.395198e-01_rb,9.390404e-01_rb,9.385728e-01_rb,9.381164e-01_rb,9.376707e-01_rb,&
        & 9.372350e-01_rb,9.368091e-01_rb,9.363923e-01_rb /)
      ssaice2(:, 22) = (/ &
! band 22
        & 9.986793e-01_rb,9.985239e-01_rb,9.983911e-01_rb,9.982715e-01_rb,9.981606e-01_rb,&
        & 9.980562e-01_rb,9.979567e-01_rb,9.978613e-01_rb,9.977691e-01_rb,9.976798e-01_rb,&
        & 9.975929e-01_rb,9.975081e-01_rb,9.974251e-01_rb,9.973438e-01_rb,9.972640e-01_rb,&
        & 9.971855e-01_rb,9.971083e-01_rb,9.970322e-01_rb,9.969571e-01_rb,9.968830e-01_rb,&
        & 9.968099e-01_rb,9.967375e-01_rb,9.966660e-01_rb,9.965951e-01_rb,9.965250e-01_rb,&
        & 9.964555e-01_rb,9.963867e-01_rb,9.963185e-01_rb,9.962508e-01_rb,9.961836e-01_rb,&
        & 9.961170e-01_rb,9.960508e-01_rb,9.959851e-01_rb,9.959198e-01_rb,9.958550e-01_rb,&
        & 9.957906e-01_rb,9.957266e-01_rb,9.956629e-01_rb,9.955997e-01_rb,9.955367e-01_rb,&
        & 9.954742e-01_rb,9.954119e-01_rb,9.953500e-01_rb /)
      ssaice2(:, 23) = (/ &
! band 23
        & 9.997944e-01_rb,9.997791e-01_rb,9.997664e-01_rb,9.997547e-01_rb,9.997436e-01_rb,&
        & 9.997327e-01_rb,9.997219e-01_rb,9.997110e-01_rb,9.996999e-01_rb,9.996886e-01_rb,&
        & 9.996771e-01_rb,9.996653e-01_rb,9.996533e-01_rb,9.996409e-01_rb,9.996282e-01_rb,&
        & 9.996152e-01_rb,9.996019e-01_rb,9.995883e-01_rb,9.995743e-01_rb,9.995599e-01_rb,&
        & 9.995453e-01_rb,9.995302e-01_rb,9.995149e-01_rb,9.994992e-01_rb,9.994831e-01_rb,&
        & 9.994667e-01_rb,9.994500e-01_rb,9.994329e-01_rb,9.994154e-01_rb,9.993976e-01_rb,&
        & 9.993795e-01_rb,9.993610e-01_rb,9.993422e-01_rb,9.993230e-01_rb,9.993035e-01_rb,&
        & 9.992837e-01_rb,9.992635e-01_rb,9.992429e-01_rb,9.992221e-01_rb,9.992008e-01_rb,&
        & 9.991793e-01_rb,9.991574e-01_rb,9.991352e-01_rb /)
      ssaice2(:, 24) = (/ &
! band 24
        & 9.999949e-01_rb,9.999947e-01_rb,9.999943e-01_rb,9.999939e-01_rb,9.999934e-01_rb,&
        & 9.999927e-01_rb,9.999920e-01_rb,9.999913e-01_rb,9.999904e-01_rb,9.999895e-01_rb,&
        & 9.999885e-01_rb,9.999874e-01_rb,9.999863e-01_rb,9.999851e-01_rb,9.999838e-01_rb,&
        & 9.999824e-01_rb,9.999810e-01_rb,9.999795e-01_rb,9.999780e-01_rb,9.999764e-01_rb,&
        & 9.999747e-01_rb,9.999729e-01_rb,9.999711e-01_rb,9.999692e-01_rb,9.999673e-01_rb,&
        & 9.999653e-01_rb,9.999632e-01_rb,9.999611e-01_rb,9.999589e-01_rb,9.999566e-01_rb,&
        & 9.999543e-01_rb,9.999519e-01_rb,9.999495e-01_rb,9.999470e-01_rb,9.999444e-01_rb,&
        & 9.999418e-01_rb,9.999392e-01_rb,9.999364e-01_rb,9.999336e-01_rb,9.999308e-01_rb,&
        & 9.999279e-01_rb,9.999249e-01_rb,9.999219e-01_rb /)
      ssaice2(:, 25) = (/ &
! band 25
        & 9.999997e-01_rb,9.999997e-01_rb,9.999997e-01_rb,9.999996e-01_rb,9.999996e-01_rb,&
        & 9.999995e-01_rb,9.999994e-01_rb,9.999993e-01_rb,9.999993e-01_rb,9.999992e-01_rb,&
        & 9.999991e-01_rb,9.999989e-01_rb,9.999988e-01_rb,9.999987e-01_rb,9.999986e-01_rb,&
        & 9.999984e-01_rb,9.999983e-01_rb,9.999981e-01_rb,9.999980e-01_rb,9.999978e-01_rb,&
        & 9.999976e-01_rb,9.999974e-01_rb,9.999972e-01_rb,9.999971e-01_rb,9.999969e-01_rb,&
        & 9.999966e-01_rb,9.999964e-01_rb,9.999962e-01_rb,9.999960e-01_rb,9.999957e-01_rb,&
        & 9.999955e-01_rb,9.999953e-01_rb,9.999950e-01_rb,9.999947e-01_rb,9.999945e-01_rb,&
        & 9.999942e-01_rb,9.999939e-01_rb,9.999936e-01_rb,9.999934e-01_rb,9.999931e-01_rb,&
        & 9.999928e-01_rb,9.999925e-01_rb,9.999921e-01_rb /)
      ssaice2(:, 26) = (/ &
! band 26
        & 9.999997e-01_rb,9.999996e-01_rb,9.999996e-01_rb,9.999995e-01_rb,9.999994e-01_rb,&
        & 9.999993e-01_rb,9.999992e-01_rb,9.999991e-01_rb,9.999990e-01_rb,9.999989e-01_rb,&
        & 9.999987e-01_rb,9.999986e-01_rb,9.999984e-01_rb,9.999982e-01_rb,9.999980e-01_rb,&
        & 9.999978e-01_rb,9.999976e-01_rb,9.999974e-01_rb,9.999972e-01_rb,9.999970e-01_rb,&
        & 9.999967e-01_rb,9.999965e-01_rb,9.999962e-01_rb,9.999959e-01_rb,9.999956e-01_rb,&
        & 9.999954e-01_rb,9.999951e-01_rb,9.999947e-01_rb,9.999944e-01_rb,9.999941e-01_rb,&
        & 9.999938e-01_rb,9.999934e-01_rb,9.999931e-01_rb,9.999927e-01_rb,9.999923e-01_rb,&
        & 9.999920e-01_rb,9.999916e-01_rb,9.999912e-01_rb,9.999908e-01_rb,9.999904e-01_rb,&
        & 9.999899e-01_rb,9.999895e-01_rb,9.999891e-01_rb /)
      ssaice2(:, 27) = (/ &
! band 27
        & 9.999987e-01_rb,9.999987e-01_rb,9.999985e-01_rb,9.999984e-01_rb,9.999982e-01_rb,&
        & 9.999980e-01_rb,9.999978e-01_rb,9.999976e-01_rb,9.999973e-01_rb,9.999970e-01_rb,&
        & 9.999967e-01_rb,9.999964e-01_rb,9.999960e-01_rb,9.999956e-01_rb,9.999952e-01_rb,&
        & 9.999948e-01_rb,9.999944e-01_rb,9.999939e-01_rb,9.999934e-01_rb,9.999929e-01_rb,&
        & 9.999924e-01_rb,9.999918e-01_rb,9.999913e-01_rb,9.999907e-01_rb,9.999901e-01_rb,&
        & 9.999894e-01_rb,9.999888e-01_rb,9.999881e-01_rb,9.999874e-01_rb,9.999867e-01_rb,&
        & 9.999860e-01_rb,9.999853e-01_rb,9.999845e-01_rb,9.999837e-01_rb,9.999829e-01_rb,&
        & 9.999821e-01_rb,9.999813e-01_rb,9.999804e-01_rb,9.999796e-01_rb,9.999787e-01_rb,&
        & 9.999778e-01_rb,9.999768e-01_rb,9.999759e-01_rb /)
      ssaice2(:, 28) = (/ &
! band 28
        & 9.999989e-01_rb,9.999989e-01_rb,9.999987e-01_rb,9.999986e-01_rb,9.999984e-01_rb,&
        & 9.999982e-01_rb,9.999980e-01_rb,9.999978e-01_rb,9.999975e-01_rb,9.999972e-01_rb,&
        & 9.999969e-01_rb,9.999966e-01_rb,9.999962e-01_rb,9.999958e-01_rb,9.999954e-01_rb,&
        & 9.999950e-01_rb,9.999945e-01_rb,9.999941e-01_rb,9.999936e-01_rb,9.999931e-01_rb,&
        & 9.999925e-01_rb,9.999920e-01_rb,9.999914e-01_rb,9.999908e-01_rb,9.999902e-01_rb,&
        & 9.999896e-01_rb,9.999889e-01_rb,9.999883e-01_rb,9.999876e-01_rb,9.999869e-01_rb,&
        & 9.999861e-01_rb,9.999854e-01_rb,9.999846e-01_rb,9.999838e-01_rb,9.999830e-01_rb,&
        & 9.999822e-01_rb,9.999814e-01_rb,9.999805e-01_rb,9.999796e-01_rb,9.999787e-01_rb,&
        & 9.999778e-01_rb,9.999769e-01_rb,9.999759e-01_rb /)
      ssaice2(:, 29) = (/ &
! band 29
        & 7.042143e-01_rb,6.691161e-01_rb,6.463240e-01_rb,6.296590e-01_rb,6.166381e-01_rb,&
        & 6.060183e-01_rb,5.970908e-01_rb,5.894144e-01_rb,5.826968e-01_rb,5.767343e-01_rb,&
        & 5.713804e-01_rb,5.665256e-01_rb,5.620867e-01_rb,5.579987e-01_rb,5.542101e-01_rb,&
        & 5.506794e-01_rb,5.473727e-01_rb,5.442620e-01_rb,5.413239e-01_rb,5.385389e-01_rb,&
        & 5.358901e-01_rb,5.333633e-01_rb,5.309460e-01_rb,5.286277e-01_rb,5.263988e-01_rb,&
        & 5.242512e-01_rb,5.221777e-01_rb,5.201719e-01_rb,5.182280e-01_rb,5.163410e-01_rb,&
        & 5.145062e-01_rb,5.127197e-01_rb,5.109776e-01_rb,5.092766e-01_rb,5.076137e-01_rb,&
        & 5.059860e-01_rb,5.043911e-01_rb,5.028266e-01_rb,5.012904e-01_rb,4.997805e-01_rb,&
        & 4.982951e-01_rb,4.968326e-01_rb,4.953913e-01_rb /)

! asymmetry factor: unitless
      asyice2(:, 16) = (/ &
! band 16
        & 7.946655e-01_rb,8.547685e-01_rb,8.806016e-01_rb,8.949880e-01_rb,9.041676e-01_rb,&
        & 9.105399e-01_rb,9.152249e-01_rb,9.188160e-01_rb,9.216573e-01_rb,9.239620e-01_rb,&
        & 9.258695e-01_rb,9.274745e-01_rb,9.288441e-01_rb,9.300267e-01_rb,9.310584e-01_rb,&
        & 9.319665e-01_rb,9.327721e-01_rb,9.334918e-01_rb,9.341387e-01_rb,9.347236e-01_rb,&
        & 9.352551e-01_rb,9.357402e-01_rb,9.361850e-01_rb,9.365942e-01_rb,9.369722e-01_rb,&
        & 9.373225e-01_rb,9.376481e-01_rb,9.379516e-01_rb,9.382352e-01_rb,9.385010e-01_rb,&
        & 9.387505e-01_rb,9.389854e-01_rb,9.392070e-01_rb,9.394163e-01_rb,9.396145e-01_rb,&
        & 9.398024e-01_rb,9.399809e-01_rb,9.401508e-01_rb,9.403126e-01_rb,9.404670e-01_rb,&
        & 9.406144e-01_rb,9.407555e-01_rb,9.408906e-01_rb /)
      asyice2(:, 17) = (/ &
! band 17
        & 9.078091e-01_rb,9.195850e-01_rb,9.267250e-01_rb,9.317083e-01_rb,9.354632e-01_rb,&
        & 9.384323e-01_rb,9.408597e-01_rb,9.428935e-01_rb,9.446301e-01_rb,9.461351e-01_rb,&
        & 9.474555e-01_rb,9.486259e-01_rb,9.496722e-01_rb,9.506146e-01_rb,9.514688e-01_rb,&
        & 9.522476e-01_rb,9.529612e-01_rb,9.536181e-01_rb,9.542251e-01_rb,9.547883e-01_rb,&
        & 9.553124e-01_rb,9.558019e-01_rb,9.562601e-01_rb,9.566904e-01_rb,9.570953e-01_rb,&
        & 9.574773e-01_rb,9.578385e-01_rb,9.581806e-01_rb,9.585054e-01_rb,9.588142e-01_rb,&
        & 9.591083e-01_rb,9.593888e-01_rb,9.596569e-01_rb,9.599135e-01_rb,9.601593e-01_rb,&
        & 9.603952e-01_rb,9.606219e-01_rb,9.608399e-01_rb,9.610499e-01_rb,9.612523e-01_rb,&
        & 9.614477e-01_rb,9.616365e-01_rb,9.618192e-01_rb /)
      asyice2(:, 18) = (/ &
! band 18
        & 8.322045e-01_rb,8.528693e-01_rb,8.648167e-01_rb,8.729163e-01_rb,8.789054e-01_rb,&
        & 8.835845e-01_rb,8.873819e-01_rb,8.905511e-01_rb,8.932532e-01_rb,8.955965e-01_rb,&
        & 8.976567e-01_rb,8.994887e-01_rb,9.011334e-01_rb,9.026221e-01_rb,9.039791e-01_rb,&
        & 9.052237e-01_rb,9.063715e-01_rb,9.074349e-01_rb,9.084245e-01_rb,9.093489e-01_rb,&
        & 9.102154e-01_rb,9.110303e-01_rb,9.117987e-01_rb,9.125253e-01_rb,9.132140e-01_rb,&
        & 9.138682e-01_rb,9.144910e-01_rb,9.150850e-01_rb,9.156524e-01_rb,9.161955e-01_rb,&
        & 9.167160e-01_rb,9.172157e-01_rb,9.176959e-01_rb,9.181581e-01_rb,9.186034e-01_rb,&
        & 9.190330e-01_rb,9.194478e-01_rb,9.198488e-01_rb,9.202368e-01_rb,9.206126e-01_rb,&
        & 9.209768e-01_rb,9.213301e-01_rb,9.216731e-01_rb /)
      asyice2(:, 19) = (/ &
! band 19
        & 8.116560e-01_rb,8.488278e-01_rb,8.674331e-01_rb,8.788148e-01_rb,8.865810e-01_rb,&
        & 8.922595e-01_rb,8.966149e-01_rb,9.000747e-01_rb,9.028980e-01_rb,9.052513e-01_rb,&
        & 9.072468e-01_rb,9.089632e-01_rb,9.104574e-01_rb,9.117713e-01_rb,9.129371e-01_rb,&
        & 9.139793e-01_rb,9.149174e-01_rb,9.157668e-01_rb,9.165400e-01_rb,9.172473e-01_rb,&
        & 9.178970e-01_rb,9.184962e-01_rb,9.190508e-01_rb,9.195658e-01_rb,9.200455e-01_rb,&
        & 9.204935e-01_rb,9.209130e-01_rb,9.213067e-01_rb,9.216771e-01_rb,9.220262e-01_rb,&
        & 9.223560e-01_rb,9.226680e-01_rb,9.229636e-01_rb,9.232443e-01_rb,9.235112e-01_rb,&
        & 9.237652e-01_rb,9.240074e-01_rb,9.242385e-01_rb,9.244594e-01_rb,9.246708e-01_rb,&
        & 9.248733e-01_rb,9.250674e-01_rb,9.252536e-01_rb /)
      asyice2(:, 20) = (/ &
! band 20
        & 8.047113e-01_rb,8.402864e-01_rb,8.570332e-01_rb,8.668455e-01_rb,8.733206e-01_rb,&
        & 8.779272e-01_rb,8.813796e-01_rb,8.840676e-01_rb,8.862225e-01_rb,8.879904e-01_rb,&
        & 8.894682e-01_rb,8.907228e-01_rb,8.918019e-01_rb,8.927404e-01_rb,8.935645e-01_rb,&
        & 8.942943e-01_rb,8.949452e-01_rb,8.955296e-01_rb,8.960574e-01_rb,8.965366e-01_rb,&
        & 8.969736e-01_rb,8.973740e-01_rb,8.977422e-01_rb,8.980820e-01_rb,8.983966e-01_rb,&
        & 8.986889e-01_rb,8.989611e-01_rb,8.992153e-01_rb,8.994533e-01_rb,8.996766e-01_rb,&
        & 8.998865e-01_rb,9.000843e-01_rb,9.002709e-01_rb,9.004474e-01_rb,9.006146e-01_rb,&
        & 9.007731e-01_rb,9.009237e-01_rb,9.010670e-01_rb,9.012034e-01_rb,9.013336e-01_rb,&
        & 9.014579e-01_rb,9.015767e-01_rb,9.016904e-01_rb /)
      asyice2(:, 21) = (/ &
! band 21
        & 8.179122e-01_rb,8.480726e-01_rb,8.621945e-01_rb,8.704354e-01_rb,8.758555e-01_rb,&
        & 8.797007e-01_rb,8.825750e-01_rb,8.848078e-01_rb,8.865939e-01_rb,8.880564e-01_rb,&
        & 8.892765e-01_rb,8.903105e-01_rb,8.911982e-01_rb,8.919689e-01_rb,8.926446e-01_rb,&
        & 8.932419e-01_rb,8.937738e-01_rb,8.942506e-01_rb,8.946806e-01_rb,8.950702e-01_rb,&
        & 8.954251e-01_rb,8.957497e-01_rb,8.960477e-01_rb,8.963223e-01_rb,8.965762e-01_rb,&
        & 8.968116e-01_rb,8.970306e-01_rb,8.972347e-01_rb,8.974255e-01_rb,8.976042e-01_rb,&
        & 8.977720e-01_rb,8.979298e-01_rb,8.980784e-01_rb,8.982188e-01_rb,8.983515e-01_rb,&
        & 8.984771e-01_rb,8.985963e-01_rb,8.987095e-01_rb,8.988171e-01_rb,8.989195e-01_rb,&
        & 8.990172e-01_rb,8.991104e-01_rb,8.991994e-01_rb /)
      asyice2(:, 22) = (/ &
! band 22
        & 8.169789e-01_rb,8.455024e-01_rb,8.586925e-01_rb,8.663283e-01_rb,8.713217e-01_rb,&
        & 8.748488e-01_rb,8.774765e-01_rb,8.795122e-01_rb,8.811370e-01_rb,8.824649e-01_rb,&
        & 8.835711e-01_rb,8.845073e-01_rb,8.853103e-01_rb,8.860068e-01_rb,8.866170e-01_rb,&
        & 8.871560e-01_rb,8.876358e-01_rb,8.880658e-01_rb,8.884533e-01_rb,8.888044e-01_rb,&
        & 8.891242e-01_rb,8.894166e-01_rb,8.896851e-01_rb,8.899324e-01_rb,8.901612e-01_rb,&
        & 8.903733e-01_rb,8.905706e-01_rb,8.907545e-01_rb,8.909265e-01_rb,8.910876e-01_rb,&
        & 8.912388e-01_rb,8.913812e-01_rb,8.915153e-01_rb,8.916419e-01_rb,8.917617e-01_rb,&
        & 8.918752e-01_rb,8.919829e-01_rb,8.920851e-01_rb,8.921824e-01_rb,8.922751e-01_rb,&
        & 8.923635e-01_rb,8.924478e-01_rb,8.925284e-01_rb /)
      asyice2(:, 23) = (/ &
! band 23
        & 8.387642e-01_rb,8.569979e-01_rb,8.658630e-01_rb,8.711825e-01_rb,8.747605e-01_rb,&
        & 8.773472e-01_rb,8.793129e-01_rb,8.808621e-01_rb,8.821179e-01_rb,8.831583e-01_rb,&
        & 8.840361e-01_rb,8.847875e-01_rb,8.854388e-01_rb,8.860094e-01_rb,8.865138e-01_rb,&
        & 8.869634e-01_rb,8.873668e-01_rb,8.877310e-01_rb,8.880617e-01_rb,8.883635e-01_rb,&
        & 8.886401e-01_rb,8.888947e-01_rb,8.891298e-01_rb,8.893477e-01_rb,8.895504e-01_rb,&
        & 8.897393e-01_rb,8.899159e-01_rb,8.900815e-01_rb,8.902370e-01_rb,8.903833e-01_rb,&
        & 8.905214e-01_rb,8.906518e-01_rb,8.907753e-01_rb,8.908924e-01_rb,8.910036e-01_rb,&
        & 8.911094e-01_rb,8.912101e-01_rb,8.913062e-01_rb,8.913979e-01_rb,8.914856e-01_rb,&
        & 8.915695e-01_rb,8.916498e-01_rb,8.917269e-01_rb /)
      asyice2(:, 24) = (/ &
! band 24
        & 8.522208e-01_rb,8.648132e-01_rb,8.711224e-01_rb,8.749901e-01_rb,8.776354e-01_rb,&
        & 8.795743e-01_rb,8.810649e-01_rb,8.822518e-01_rb,8.832225e-01_rb,8.840333e-01_rb,&
        & 8.847224e-01_rb,8.853162e-01_rb,8.858342e-01_rb,8.862906e-01_rb,8.866962e-01_rb,&
        & 8.870595e-01_rb,8.873871e-01_rb,8.876842e-01_rb,8.879551e-01_rb,8.882032e-01_rb,&
        & 8.884316e-01_rb,8.886425e-01_rb,8.888380e-01_rb,8.890199e-01_rb,8.891895e-01_rb,&
        & 8.893481e-01_rb,8.894968e-01_rb,8.896366e-01_rb,8.897683e-01_rb,8.898926e-01_rb,&
        & 8.900102e-01_rb,8.901215e-01_rb,8.902272e-01_rb,8.903276e-01_rb,8.904232e-01_rb,&
        & 8.905144e-01_rb,8.906014e-01_rb,8.906845e-01_rb,8.907640e-01_rb,8.908402e-01_rb,&
        & 8.909132e-01_rb,8.909834e-01_rb,8.910507e-01_rb /)
      asyice2(:, 25) = (/ &
! band 25
        & 8.578202e-01_rb,8.683033e-01_rb,8.735431e-01_rb,8.767488e-01_rb,8.789378e-01_rb,&
        & 8.805399e-01_rb,8.817701e-01_rb,8.827485e-01_rb,8.835480e-01_rb,8.842152e-01_rb,&
        & 8.847817e-01_rb,8.852696e-01_rb,8.856949e-01_rb,8.860694e-01_rb,8.864020e-01_rb,&
        & 8.866997e-01_rb,8.869681e-01_rb,8.872113e-01_rb,8.874330e-01_rb,8.876360e-01_rb,&
        & 8.878227e-01_rb,8.879951e-01_rb,8.881548e-01_rb,8.883033e-01_rb,8.884418e-01_rb,&
        & 8.885712e-01_rb,8.886926e-01_rb,8.888066e-01_rb,8.889139e-01_rb,8.890152e-01_rb,&
        & 8.891110e-01_rb,8.892017e-01_rb,8.892877e-01_rb,8.893695e-01_rb,8.894473e-01_rb,&
        & 8.895214e-01_rb,8.895921e-01_rb,8.896597e-01_rb,8.897243e-01_rb,8.897862e-01_rb,&
        & 8.898456e-01_rb,8.899025e-01_rb,8.899572e-01_rb /)
      asyice2(:, 26) = (/ &
! band 26
        & 8.625615e-01_rb,8.713831e-01_rb,8.755799e-01_rb,8.780560e-01_rb,8.796983e-01_rb,&
        & 8.808714e-01_rb,8.817534e-01_rb,8.824420e-01_rb,8.829953e-01_rb,8.834501e-01_rb,&
        & 8.838310e-01_rb,8.841549e-01_rb,8.844338e-01_rb,8.846767e-01_rb,8.848902e-01_rb,&
        & 8.850795e-01_rb,8.852484e-01_rb,8.854002e-01_rb,8.855374e-01_rb,8.856620e-01_rb,&
        & 8.857758e-01_rb,8.858800e-01_rb,8.859759e-01_rb,8.860644e-01_rb,8.861464e-01_rb,&
        & 8.862225e-01_rb,8.862935e-01_rb,8.863598e-01_rb,8.864218e-01_rb,8.864800e-01_rb,&
        & 8.865347e-01_rb,8.865863e-01_rb,8.866349e-01_rb,8.866809e-01_rb,8.867245e-01_rb,&
        & 8.867658e-01_rb,8.868050e-01_rb,8.868423e-01_rb,8.868778e-01_rb,8.869117e-01_rb,&
        & 8.869440e-01_rb,8.869749e-01_rb,8.870044e-01_rb /)
      asyice2(:, 27) = (/ &
! band 27
        & 8.587495e-01_rb,8.684764e-01_rb,8.728189e-01_rb,8.752872e-01_rb,8.768846e-01_rb,&
        & 8.780060e-01_rb,8.788386e-01_rb,8.794824e-01_rb,8.799960e-01_rb,8.804159e-01_rb,&
        & 8.807660e-01_rb,8.810626e-01_rb,8.813175e-01_rb,8.815390e-01_rb,8.817335e-01_rb,&
        & 8.819057e-01_rb,8.820593e-01_rb,8.821973e-01_rb,8.823220e-01_rb,8.824353e-01_rb,&
        & 8.825387e-01_rb,8.826336e-01_rb,8.827209e-01_rb,8.828016e-01_rb,8.828764e-01_rb,&
        & 8.829459e-01_rb,8.830108e-01_rb,8.830715e-01_rb,8.831283e-01_rb,8.831817e-01_rb,&
        & 8.832320e-01_rb,8.832795e-01_rb,8.833244e-01_rb,8.833668e-01_rb,8.834071e-01_rb,&
        & 8.834454e-01_rb,8.834817e-01_rb,8.835164e-01_rb,8.835495e-01_rb,8.835811e-01_rb,&
        & 8.836113e-01_rb,8.836402e-01_rb,8.836679e-01_rb /)
      asyice2(:, 28) = (/ &
! band 28
        & 8.561110e-01_rb,8.678583e-01_rb,8.727554e-01_rb,8.753892e-01_rb,8.770154e-01_rb,&
        & 8.781109e-01_rb,8.788949e-01_rb,8.794812e-01_rb,8.799348e-01_rb,8.802952e-01_rb,&
        & 8.805880e-01_rb,8.808300e-01_rb,8.810331e-01_rb,8.812058e-01_rb,8.813543e-01_rb,&
        & 8.814832e-01_rb,8.815960e-01_rb,8.816956e-01_rb,8.817839e-01_rb,8.818629e-01_rb,&
        & 8.819339e-01_rb,8.819979e-01_rb,8.820560e-01_rb,8.821089e-01_rb,8.821573e-01_rb,&
        & 8.822016e-01_rb,8.822425e-01_rb,8.822801e-01_rb,8.823150e-01_rb,8.823474e-01_rb,&
        & 8.823775e-01_rb,8.824056e-01_rb,8.824318e-01_rb,8.824564e-01_rb,8.824795e-01_rb,&
        & 8.825011e-01_rb,8.825215e-01_rb,8.825408e-01_rb,8.825589e-01_rb,8.825761e-01_rb,&
        & 8.825924e-01_rb,8.826078e-01_rb,8.826224e-01_rb /)
      asyice2(:, 29) = (/ &
! band 29
        & 8.311124e-01_rb,8.688197e-01_rb,8.900274e-01_rb,9.040696e-01_rb,9.142334e-01_rb,&
        & 9.220181e-01_rb,9.282195e-01_rb,9.333048e-01_rb,9.375689e-01_rb,9.412085e-01_rb,&
        & 9.443604e-01_rb,9.471230e-01_rb,9.495694e-01_rb,9.517549e-01_rb,9.537224e-01_rb,&
        & 9.555057e-01_rb,9.571316e-01_rb,9.586222e-01_rb,9.599952e-01_rb,9.612656e-01_rb,&
        & 9.624458e-01_rb,9.635461e-01_rb,9.645756e-01_rb,9.655418e-01_rb,9.664513e-01_rb,&
        & 9.673098e-01_rb,9.681222e-01_rb,9.688928e-01_rb,9.696256e-01_rb,9.703237e-01_rb,&
        & 9.709903e-01_rb,9.716280e-01_rb,9.722391e-01_rb,9.728258e-01_rb,9.733901e-01_rb,&
        & 9.739336e-01_rb,9.744579e-01_rb,9.749645e-01_rb,9.754546e-01_rb,9.759294e-01_rb,&
        & 9.763901e-01_rb,9.768376e-01_rb,9.772727e-01_rb /)

! Hexagonal Ice Particle Parameterization
! extinction units (ext coef/iwc): [(m^-1)/(g m^-3)]
      extice3(:, 16) = (/ &
! band 16
        & 5.194013e-01_rb,3.215089e-01_rb,2.327917e-01_rb,1.824424e-01_rb,1.499977e-01_rb,&
        & 1.273492e-01_rb,1.106421e-01_rb,9.780982e-02_rb,8.764435e-02_rb,7.939266e-02_rb,&
        & 7.256081e-02_rb,6.681137e-02_rb,6.190600e-02_rb,5.767154e-02_rb,5.397915e-02_rb,&
        & 5.073102e-02_rb,4.785151e-02_rb,4.528125e-02_rb,4.297296e-02_rb,4.088853e-02_rb,&
        & 3.899690e-02_rb,3.727251e-02_rb,3.569411e-02_rb,3.424393e-02_rb,3.290694e-02_rb,&
        & 3.167040e-02_rb,3.052340e-02_rb,2.945654e-02_rb,2.846172e-02_rb,2.753188e-02_rb,&
        & 2.666085e-02_rb,2.584322e-02_rb,2.507423e-02_rb,2.434967e-02_rb,2.366579e-02_rb,&
        & 2.301926e-02_rb,2.240711e-02_rb,2.182666e-02_rb,2.127551e-02_rb,2.075150e-02_rb,&
        & 2.025267e-02_rb,1.977725e-02_rb,1.932364e-02_rb,1.889035e-02_rb,1.847607e-02_rb,&
        & 1.807956e-02_rb /)
      extice3(:, 17) = (/ &
! band 17
        & 4.901155e-01_rb,3.065286e-01_rb,2.230800e-01_rb,1.753951e-01_rb,1.445402e-01_rb,&
        & 1.229417e-01_rb,1.069777e-01_rb,9.469760e-02_rb,8.495824e-02_rb,7.704501e-02_rb,&
        & 7.048834e-02_rb,6.496693e-02_rb,6.025353e-02_rb,5.618286e-02_rb,5.263186e-02_rb,&
        & 4.950698e-02_rb,4.673585e-02_rb,4.426164e-02_rb,4.203904e-02_rb,4.003153e-02_rb,&
        & 3.820932e-02_rb,3.654790e-02_rb,3.502688e-02_rb,3.362919e-02_rb,3.234041e-02_rb,&
        & 3.114829e-02_rb,3.004234e-02_rb,2.901356e-02_rb,2.805413e-02_rb,2.715727e-02_rb,&
        & 2.631705e-02_rb,2.552828e-02_rb,2.478637e-02_rb,2.408725e-02_rb,2.342734e-02_rb,&
        & 2.280343e-02_rb,2.221264e-02_rb,2.165242e-02_rb,2.112043e-02_rb,2.061461e-02_rb,&
        & 2.013308e-02_rb,1.967411e-02_rb,1.923616e-02_rb,1.881783e-02_rb,1.841781e-02_rb,&
        & 1.803494e-02_rb /)
      extice3(:, 18) = (/ &
! band 18
        & 5.056264e-01_rb,3.160261e-01_rb,2.298442e-01_rb,1.805973e-01_rb,1.487318e-01_rb,&
        & 1.264258e-01_rb,1.099389e-01_rb,9.725656e-02_rb,8.719819e-02_rb,7.902576e-02_rb,&
        & 7.225433e-02_rb,6.655206e-02_rb,6.168427e-02_rb,5.748028e-02_rb,5.381296e-02_rb,&
        & 5.058572e-02_rb,4.772383e-02_rb,4.516857e-02_rb,4.287317e-02_rb,4.079990e-02_rb,&
        & 3.891801e-02_rb,3.720217e-02_rb,3.563133e-02_rb,3.418786e-02_rb,3.285686e-02_rb,&
        & 3.162569e-02_rb,3.048352e-02_rb,2.942104e-02_rb,2.843018e-02_rb,2.750395e-02_rb,&
        & 2.663621e-02_rb,2.582160e-02_rb,2.505539e-02_rb,2.433337e-02_rb,2.365185e-02_rb,&
        & 2.300750e-02_rb,2.239736e-02_rb,2.181878e-02_rb,2.126937e-02_rb,2.074699e-02_rb,&
        & 2.024968e-02_rb,1.977567e-02_rb,1.932338e-02_rb,1.889134e-02_rb,1.847823e-02_rb,&
        & 1.808281e-02_rb /)
      extice3(:, 19) = (/ &
! band 19
        & 4.881605e-01_rb,3.055237e-01_rb,2.225070e-01_rb,1.750688e-01_rb,1.443736e-01_rb,&
        & 1.228869e-01_rb,1.070054e-01_rb,9.478893e-02_rb,8.509997e-02_rb,7.722769e-02_rb,&
        & 7.070495e-02_rb,6.521211e-02_rb,6.052311e-02_rb,5.647351e-02_rb,5.294088e-02_rb,&
        & 4.983217e-02_rb,4.707539e-02_rb,4.461398e-02_rb,4.240288e-02_rb,4.040575e-02_rb,&
        & 3.859298e-02_rb,3.694016e-02_rb,3.542701e-02_rb,3.403655e-02_rb,3.275444e-02_rb,&
        & 3.156849e-02_rb,3.046827e-02_rb,2.944481e-02_rb,2.849034e-02_rb,2.759812e-02_rb,&
        & 2.676226e-02_rb,2.597757e-02_rb,2.523949e-02_rb,2.454400e-02_rb,2.388750e-02_rb,&
        & 2.326682e-02_rb,2.267909e-02_rb,2.212176e-02_rb,2.159253e-02_rb,2.108933e-02_rb,&
        & 2.061028e-02_rb,2.015369e-02_rb,1.971801e-02_rb,1.930184e-02_rb,1.890389e-02_rb,&
        & 1.852300e-02_rb /)
      extice3(:, 20) = (/ &
! band 20
        & 5.103703e-01_rb,3.188144e-01_rb,2.317435e-01_rb,1.819887e-01_rb,1.497944e-01_rb,&
        & 1.272584e-01_rb,1.106013e-01_rb,9.778822e-02_rb,8.762610e-02_rb,7.936938e-02_rb,&
        & 7.252809e-02_rb,6.676701e-02_rb,6.184901e-02_rb,5.760165e-02_rb,5.389651e-02_rb,&
        & 5.063598e-02_rb,4.774457e-02_rb,4.516295e-02_rb,4.284387e-02_rb,4.074922e-02_rb,&
        & 3.884792e-02_rb,3.711438e-02_rb,3.552734e-02_rb,3.406898e-02_rb,3.272425e-02_rb,&
        & 3.148038e-02_rb,3.032643e-02_rb,2.925299e-02_rb,2.825191e-02_rb,2.731612e-02_rb,&
        & 2.643943e-02_rb,2.561642e-02_rb,2.484230e-02_rb,2.411284e-02_rb,2.342429e-02_rb,&
        & 2.277329e-02_rb,2.215686e-02_rb,2.157231e-02_rb,2.101724e-02_rb,2.048946e-02_rb,&
        & 1.998702e-02_rb,1.950813e-02_rb,1.905118e-02_rb,1.861468e-02_rb,1.819730e-02_rb,&
        & 1.779781e-02_rb /)
      extice3(:, 21) = (/ &
! band 21
        & 5.031161e-01_rb,3.144511e-01_rb,2.286942e-01_rb,1.796903e-01_rb,1.479819e-01_rb,&
        & 1.257860e-01_rb,1.093803e-01_rb,9.676059e-02_rb,8.675183e-02_rb,7.861971e-02_rb,&
        & 7.188168e-02_rb,6.620754e-02_rb,6.136376e-02_rb,5.718050e-02_rb,5.353127e-02_rb,&
        & 5.031995e-02_rb,4.747218e-02_rb,4.492952e-02_rb,4.264544e-02_rb,4.058240e-02_rb,&
        & 3.870979e-02_rb,3.700242e-02_rb,3.543933e-02_rb,3.400297e-02_rb,3.267854e-02_rb,&
        & 3.145345e-02_rb,3.031691e-02_rb,2.925967e-02_rb,2.827370e-02_rb,2.735203e-02_rb,&
        & 2.648858e-02_rb,2.567798e-02_rb,2.491555e-02_rb,2.419710e-02_rb,2.351893e-02_rb,&
        & 2.287776e-02_rb,2.227063e-02_rb,2.169491e-02_rb,2.114821e-02_rb,2.062840e-02_rb,&
        & 2.013354e-02_rb,1.966188e-02_rb,1.921182e-02_rb,1.878191e-02_rb,1.837083e-02_rb,&
        & 1.797737e-02_rb /)
      extice3(:, 22) = (/ &
! band 22
        & 4.949453e-01_rb,3.095918e-01_rb,2.253402e-01_rb,1.771964e-01_rb,1.460446e-01_rb,&
        & 1.242383e-01_rb,1.081206e-01_rb,9.572235e-02_rb,8.588928e-02_rb,7.789990e-02_rb,&
        & 7.128013e-02_rb,6.570559e-02_rb,6.094684e-02_rb,5.683701e-02_rb,5.325183e-02_rb,&
        & 5.009688e-02_rb,4.729909e-02_rb,4.480106e-02_rb,4.255708e-02_rb,4.053025e-02_rb,&
        & 3.869051e-02_rb,3.701310e-02_rb,3.547745e-02_rb,3.406631e-02_rb,3.276512e-02_rb,&
        & 3.156153e-02_rb,3.044494e-02_rb,2.940626e-02_rb,2.843759e-02_rb,2.753211e-02_rb,&
        & 2.668381e-02_rb,2.588744e-02_rb,2.513839e-02_rb,2.443255e-02_rb,2.376629e-02_rb,&
        & 2.313637e-02_rb,2.253990e-02_rb,2.197428e-02_rb,2.143718e-02_rb,2.092649e-02_rb,&
        & 2.044032e-02_rb,1.997694e-02_rb,1.953478e-02_rb,1.911241e-02_rb,1.870855e-02_rb,&
        & 1.832199e-02_rb /)
      extice3(:, 23) = (/ &
! band 23
        & 5.052816e-01_rb,3.157665e-01_rb,2.296233e-01_rb,1.803986e-01_rb,1.485473e-01_rb,&
        & 1.262514e-01_rb,1.097718e-01_rb,9.709524e-02_rb,8.704139e-02_rb,7.887264e-02_rb,&
        & 7.210424e-02_rb,6.640454e-02_rb,6.153894e-02_rb,5.733683e-02_rb,5.367116e-02_rb,&
        & 5.044537e-02_rb,4.758477e-02_rb,4.503066e-02_rb,4.273629e-02_rb,4.066395e-02_rb,&
        & 3.878291e-02_rb,3.706784e-02_rb,3.549771e-02_rb,3.405488e-02_rb,3.272448e-02_rb,&
        & 3.149387e-02_rb,3.035221e-02_rb,2.929020e-02_rb,2.829979e-02_rb,2.737397e-02_rb,&
        & 2.650663e-02_rb,2.569238e-02_rb,2.492651e-02_rb,2.420482e-02_rb,2.352361e-02_rb,&
        & 2.287954e-02_rb,2.226968e-02_rb,2.169136e-02_rb,2.114220e-02_rb,2.062005e-02_rb,&
        & 2.012296e-02_rb,1.964917e-02_rb,1.919709e-02_rb,1.876524e-02_rb,1.835231e-02_rb,&
        & 1.795707e-02_rb /)
      extice3(:, 24) = (/ &
! band 24
        & 5.042067e-01_rb,3.151195e-01_rb,2.291708e-01_rb,1.800573e-01_rb,1.482779e-01_rb,&
        & 1.260324e-01_rb,1.095900e-01_rb,9.694202e-02_rb,8.691087e-02_rb,7.876056e-02_rb,&
        & 7.200745e-02_rb,6.632062e-02_rb,6.146600e-02_rb,5.727338e-02_rb,5.361599e-02_rb,&
        & 5.039749e-02_rb,4.754334e-02_rb,4.499500e-02_rb,4.270580e-02_rb,4.063815e-02_rb,&
        & 3.876135e-02_rb,3.705016e-02_rb,3.548357e-02_rb,3.404400e-02_rb,3.271661e-02_rb,&
        & 3.148877e-02_rb,3.034969e-02_rb,2.929008e-02_rb,2.830191e-02_rb,2.737818e-02_rb,&
        & 2.651279e-02_rb,2.570039e-02_rb,2.493624e-02_rb,2.421618e-02_rb,2.353650e-02_rb,&
        & 2.289390e-02_rb,2.228541e-02_rb,2.170840e-02_rb,2.116048e-02_rb,2.063950e-02_rb,&
        & 2.014354e-02_rb,1.967082e-02_rb,1.921975e-02_rb,1.878888e-02_rb,1.837688e-02_rb,&
        & 1.798254e-02_rb /)
      extice3(:, 25) = (/ &
! band 25
        & 5.022507e-01_rb,3.139246e-01_rb,2.283218e-01_rb,1.794059e-01_rb,1.477544e-01_rb,&
        & 1.255984e-01_rb,1.092222e-01_rb,9.662516e-02_rb,8.663439e-02_rb,7.851688e-02_rb,&
        & 7.179095e-02_rb,6.612700e-02_rb,6.129193e-02_rb,5.711618e-02_rb,5.347351e-02_rb,&
        & 5.026796e-02_rb,4.742530e-02_rb,4.488721e-02_rb,4.260724e-02_rb,4.054790e-02_rb,&
        & 3.867866e-02_rb,3.697435e-02_rb,3.541407e-02_rb,3.398029e-02_rb,3.265824e-02_rb,&
        & 3.143535e-02_rb,3.030085e-02_rb,2.924551e-02_rb,2.826131e-02_rb,2.734130e-02_rb,&
        & 2.647939e-02_rb,2.567026e-02_rb,2.490919e-02_rb,2.419203e-02_rb,2.351509e-02_rb,&
        & 2.287507e-02_rb,2.226903e-02_rb,2.169434e-02_rb,2.114862e-02_rb,2.062975e-02_rb,&
        & 2.013578e-02_rb,1.966496e-02_rb,1.921571e-02_rb,1.878658e-02_rb,1.837623e-02_rb,&
        & 1.798348e-02_rb /)
      extice3(:, 26) = (/ &
! band 26
        & 5.068316e-01_rb,3.166869e-01_rb,2.302576e-01_rb,1.808693e-01_rb,1.489122e-01_rb,&
        & 1.265423e-01_rb,1.100080e-01_rb,9.728926e-02_rb,8.720201e-02_rb,7.900612e-02_rb,&
        & 7.221524e-02_rb,6.649660e-02_rb,6.161484e-02_rb,5.739877e-02_rb,5.372093e-02_rb,&
        & 5.048442e-02_rb,4.761431e-02_rb,4.505172e-02_rb,4.274972e-02_rb,4.067050e-02_rb,&
        & 3.878321e-02_rb,3.706244e-02_rb,3.548710e-02_rb,3.403948e-02_rb,3.270466e-02_rb,&
        & 3.146995e-02_rb,3.032450e-02_rb,2.925897e-02_rb,2.826527e-02_rb,2.733638e-02_rb,&
        & 2.646615e-02_rb,2.564920e-02_rb,2.488078e-02_rb,2.415670e-02_rb,2.347322e-02_rb,&
        & 2.282702e-02_rb,2.221513e-02_rb,2.163489e-02_rb,2.108390e-02_rb,2.056002e-02_rb,&
        & 2.006128e-02_rb,1.958591e-02_rb,1.913232e-02_rb,1.869904e-02_rb,1.828474e-02_rb,&
        & 1.788819e-02_rb /)
      extice3(:, 27) = (/ &
! band 27
        & 5.077707e-01_rb,3.172636e-01_rb,2.306695e-01_rb,1.811871e-01_rb,1.491691e-01_rb,&
        & 1.267565e-01_rb,1.101907e-01_rb,9.744773e-02_rb,8.734125e-02_rb,7.912973e-02_rb,&
        & 7.232591e-02_rb,6.659637e-02_rb,6.170530e-02_rb,5.748120e-02_rb,5.379634e-02_rb,&
        & 5.055367e-02_rb,4.767809e-02_rb,4.511061e-02_rb,4.280423e-02_rb,4.072104e-02_rb,&
        & 3.883015e-02_rb,3.710611e-02_rb,3.552776e-02_rb,3.407738e-02_rb,3.274002e-02_rb,&
        & 3.150296e-02_rb,3.035532e-02_rb,2.928776e-02_rb,2.829216e-02_rb,2.736150e-02_rb,&
        & 2.648961e-02_rb,2.567111e-02_rb,2.490123e-02_rb,2.417576e-02_rb,2.349098e-02_rb,&
        & 2.284354e-02_rb,2.223049e-02_rb,2.164914e-02_rb,2.109711e-02_rb,2.057222e-02_rb,&
        & 2.007253e-02_rb,1.959626e-02_rb,1.914181e-02_rb,1.870770e-02_rb,1.829261e-02_rb,&
        & 1.789531e-02_rb /)
      extice3(:, 28) = (/ &
! band 28
        & 5.062281e-01_rb,3.163402e-01_rb,2.300275e-01_rb,1.807060e-01_rb,1.487921e-01_rb,&
        & 1.264523e-01_rb,1.099403e-01_rb,9.723879e-02_rb,8.716516e-02_rb,7.898034e-02_rb,&
        & 7.219863e-02_rb,6.648771e-02_rb,6.161254e-02_rb,5.740217e-02_rb,5.372929e-02_rb,&
        & 5.049716e-02_rb,4.763092e-02_rb,4.507179e-02_rb,4.277290e-02_rb,4.069649e-02_rb,&
        & 3.881175e-02_rb,3.709331e-02_rb,3.552008e-02_rb,3.407442e-02_rb,3.274141e-02_rb,&
        & 3.150837e-02_rb,3.036447e-02_rb,2.930037e-02_rb,2.830801e-02_rb,2.738037e-02_rb,&
        & 2.651132e-02_rb,2.569547e-02_rb,2.492810e-02_rb,2.420499e-02_rb,2.352243e-02_rb,&
        & 2.287710e-02_rb,2.226604e-02_rb,2.168658e-02_rb,2.113634e-02_rb,2.061316e-02_rb,&
        & 2.011510e-02_rb,1.964038e-02_rb,1.918740e-02_rb,1.875471e-02_rb,1.834096e-02_rb,&
        & 1.794495e-02_rb /)
      extice3(:, 29) = (/ &
! band 29
        & 1.338834e-01_rb,1.924912e-01_rb,1.755523e-01_rb,1.534793e-01_rb,1.343937e-01_rb,&
        & 1.187883e-01_rb,1.060654e-01_rb,9.559106e-02_rb,8.685880e-02_rb,7.948698e-02_rb,&
        & 7.319086e-02_rb,6.775669e-02_rb,6.302215e-02_rb,5.886236e-02_rb,5.517996e-02_rb,&
        & 5.189810e-02_rb,4.895539e-02_rb,4.630225e-02_rb,4.389823e-02_rb,4.171002e-02_rb,&
        & 3.970998e-02_rb,3.787493e-02_rb,3.618537e-02_rb,3.462471e-02_rb,3.317880e-02_rb,&
        & 3.183547e-02_rb,3.058421e-02_rb,2.941590e-02_rb,2.832256e-02_rb,2.729724e-02_rb,&
        & 2.633377e-02_rb,2.542675e-02_rb,2.457136e-02_rb,2.376332e-02_rb,2.299882e-02_rb,&
        & 2.227443e-02_rb,2.158707e-02_rb,2.093400e-02_rb,2.031270e-02_rb,1.972091e-02_rb,&
        & 1.915659e-02_rb,1.861787e-02_rb,1.810304e-02_rb,1.761055e-02_rb,1.713899e-02_rb,&
        & 1.668704e-02_rb /)

! single-scattering albedo: unitless
      ssaice3(:, 16) = (/ &
! band 16
        & 6.749442e-01_rb,6.649947e-01_rb,6.565828e-01_rb,6.489928e-01_rb,6.420046e-01_rb,&
        & 6.355231e-01_rb,6.294964e-01_rb,6.238901e-01_rb,6.186783e-01_rb,6.138395e-01_rb,&
        & 6.093543e-01_rb,6.052049e-01_rb,6.013742e-01_rb,5.978457e-01_rb,5.946030e-01_rb,&
        & 5.916302e-01_rb,5.889115e-01_rb,5.864310e-01_rb,5.841731e-01_rb,5.821221e-01_rb,&
        & 5.802624e-01_rb,5.785785e-01_rb,5.770549e-01_rb,5.756759e-01_rb,5.744262e-01_rb,&
        & 5.732901e-01_rb,5.722524e-01_rb,5.712974e-01_rb,5.704097e-01_rb,5.695739e-01_rb,&
        & 5.687747e-01_rb,5.679964e-01_rb,5.672238e-01_rb,5.664415e-01_rb,5.656340e-01_rb,&
        & 5.647860e-01_rb,5.638821e-01_rb,5.629070e-01_rb,5.618452e-01_rb,5.606815e-01_rb,&
        & 5.594006e-01_rb,5.579870e-01_rb,5.564255e-01_rb,5.547008e-01_rb,5.527976e-01_rb,&
        & 5.507005e-01_rb /)
      ssaice3(:, 17) = (/ &
! band 17
        & 7.628550e-01_rb,7.567297e-01_rb,7.508463e-01_rb,7.451972e-01_rb,7.397745e-01_rb,&
        & 7.345705e-01_rb,7.295775e-01_rb,7.247881e-01_rb,7.201945e-01_rb,7.157894e-01_rb,&
        & 7.115652e-01_rb,7.075145e-01_rb,7.036300e-01_rb,6.999044e-01_rb,6.963304e-01_rb,&
        & 6.929007e-01_rb,6.896083e-01_rb,6.864460e-01_rb,6.834067e-01_rb,6.804833e-01_rb,&
        & 6.776690e-01_rb,6.749567e-01_rb,6.723397e-01_rb,6.698109e-01_rb,6.673637e-01_rb,&
        & 6.649913e-01_rb,6.626870e-01_rb,6.604441e-01_rb,6.582561e-01_rb,6.561163e-01_rb,&
        & 6.540182e-01_rb,6.519554e-01_rb,6.499215e-01_rb,6.479099e-01_rb,6.459145e-01_rb,&
        & 6.439289e-01_rb,6.419468e-01_rb,6.399621e-01_rb,6.379686e-01_rb,6.359601e-01_rb,&
        & 6.339306e-01_rb,6.318740e-01_rb,6.297845e-01_rb,6.276559e-01_rb,6.254825e-01_rb,&
        & 6.232583e-01_rb /)
      ssaice3(:, 18) = (/ &
! band 18
        & 9.924147e-01_rb,9.882792e-01_rb,9.842257e-01_rb,9.802522e-01_rb,9.763566e-01_rb,&
        & 9.725367e-01_rb,9.687905e-01_rb,9.651157e-01_rb,9.615104e-01_rb,9.579725e-01_rb,&
        & 9.544997e-01_rb,9.510901e-01_rb,9.477416e-01_rb,9.444520e-01_rb,9.412194e-01_rb,&
        & 9.380415e-01_rb,9.349165e-01_rb,9.318421e-01_rb,9.288164e-01_rb,9.258373e-01_rb,&
        & 9.229027e-01_rb,9.200106e-01_rb,9.171589e-01_rb,9.143457e-01_rb,9.115688e-01_rb,&
        & 9.088263e-01_rb,9.061161e-01_rb,9.034362e-01_rb,9.007846e-01_rb,8.981592e-01_rb,&
        & 8.955581e-01_rb,8.929792e-01_rb,8.904206e-01_rb,8.878803e-01_rb,8.853562e-01_rb,&
        & 8.828464e-01_rb,8.803488e-01_rb,8.778616e-01_rb,8.753827e-01_rb,8.729102e-01_rb,&
        & 8.704421e-01_rb,8.679764e-01_rb,8.655112e-01_rb,8.630445e-01_rb,8.605744e-01_rb,&
        & 8.580989e-01_rb /)
      ssaice3(:, 19) = (/ &
! band 19
        & 9.629413e-01_rb,9.517182e-01_rb,9.409209e-01_rb,9.305366e-01_rb,9.205529e-01_rb,&
        & 9.109569e-01_rb,9.017362e-01_rb,8.928780e-01_rb,8.843699e-01_rb,8.761992e-01_rb,&
        & 8.683536e-01_rb,8.608204e-01_rb,8.535873e-01_rb,8.466417e-01_rb,8.399712e-01_rb,&
        & 8.335635e-01_rb,8.274062e-01_rb,8.214868e-01_rb,8.157932e-01_rb,8.103129e-01_rb,&
        & 8.050336e-01_rb,7.999432e-01_rb,7.950294e-01_rb,7.902798e-01_rb,7.856825e-01_rb,&
        & 7.812250e-01_rb,7.768954e-01_rb,7.726815e-01_rb,7.685711e-01_rb,7.645522e-01_rb,&
        & 7.606126e-01_rb,7.567404e-01_rb,7.529234e-01_rb,7.491498e-01_rb,7.454074e-01_rb,&
        & 7.416844e-01_rb,7.379688e-01_rb,7.342485e-01_rb,7.305118e-01_rb,7.267468e-01_rb,&
        & 7.229415e-01_rb,7.190841e-01_rb,7.151628e-01_rb,7.111657e-01_rb,7.070811e-01_rb,&
        & 7.028972e-01_rb /)
      ssaice3(:, 20) = (/ &
! band 20
        & 9.942270e-01_rb,9.909206e-01_rb,9.876775e-01_rb,9.844960e-01_rb,9.813746e-01_rb,&
        & 9.783114e-01_rb,9.753049e-01_rb,9.723535e-01_rb,9.694553e-01_rb,9.666088e-01_rb,&
        & 9.638123e-01_rb,9.610641e-01_rb,9.583626e-01_rb,9.557060e-01_rb,9.530928e-01_rb,&
        & 9.505211e-01_rb,9.479895e-01_rb,9.454961e-01_rb,9.430393e-01_rb,9.406174e-01_rb,&
        & 9.382288e-01_rb,9.358717e-01_rb,9.335446e-01_rb,9.312456e-01_rb,9.289731e-01_rb,&
        & 9.267255e-01_rb,9.245010e-01_rb,9.222980e-01_rb,9.201147e-01_rb,9.179496e-01_rb,&
        & 9.158008e-01_rb,9.136667e-01_rb,9.115457e-01_rb,9.094359e-01_rb,9.073358e-01_rb,&
        & 9.052436e-01_rb,9.031577e-01_rb,9.010763e-01_rb,8.989977e-01_rb,8.969203e-01_rb,&
        & 8.948423e-01_rb,8.927620e-01_rb,8.906778e-01_rb,8.885879e-01_rb,8.864907e-01_rb,&
        & 8.843843e-01_rb /)
      ssaice3(:, 21) = (/ &
! band 21
        & 9.934014e-01_rb,9.899331e-01_rb,9.865537e-01_rb,9.832610e-01_rb,9.800523e-01_rb,&
        & 9.769254e-01_rb,9.738777e-01_rb,9.709069e-01_rb,9.680106e-01_rb,9.651862e-01_rb,&
        & 9.624315e-01_rb,9.597439e-01_rb,9.571212e-01_rb,9.545608e-01_rb,9.520605e-01_rb,&
        & 9.496177e-01_rb,9.472301e-01_rb,9.448954e-01_rb,9.426111e-01_rb,9.403749e-01_rb,&
        & 9.381843e-01_rb,9.360370e-01_rb,9.339307e-01_rb,9.318629e-01_rb,9.298313e-01_rb,&
        & 9.278336e-01_rb,9.258673e-01_rb,9.239302e-01_rb,9.220198e-01_rb,9.201338e-01_rb,&
        & 9.182700e-01_rb,9.164258e-01_rb,9.145991e-01_rb,9.127874e-01_rb,9.109884e-01_rb,&
        & 9.091999e-01_rb,9.074194e-01_rb,9.056447e-01_rb,9.038735e-01_rb,9.021033e-01_rb,&
        & 9.003320e-01_rb,8.985572e-01_rb,8.967766e-01_rb,8.949879e-01_rb,8.931888e-01_rb,&
        & 8.913770e-01_rb /)
      ssaice3(:, 22) = (/ &
! band 22
        & 9.994833e-01_rb,9.992055e-01_rb,9.989278e-01_rb,9.986500e-01_rb,9.983724e-01_rb,&
        & 9.980947e-01_rb,9.978172e-01_rb,9.975397e-01_rb,9.972623e-01_rb,9.969849e-01_rb,&
        & 9.967077e-01_rb,9.964305e-01_rb,9.961535e-01_rb,9.958765e-01_rb,9.955997e-01_rb,&
        & 9.953230e-01_rb,9.950464e-01_rb,9.947699e-01_rb,9.944936e-01_rb,9.942174e-01_rb,&
        & 9.939414e-01_rb,9.936656e-01_rb,9.933899e-01_rb,9.931144e-01_rb,9.928390e-01_rb,&
        & 9.925639e-01_rb,9.922889e-01_rb,9.920141e-01_rb,9.917396e-01_rb,9.914652e-01_rb,&
        & 9.911911e-01_rb,9.909171e-01_rb,9.906434e-01_rb,9.903700e-01_rb,9.900967e-01_rb,&
        & 9.898237e-01_rb,9.895510e-01_rb,9.892784e-01_rb,9.890062e-01_rb,9.887342e-01_rb,&
        & 9.884625e-01_rb,9.881911e-01_rb,9.879199e-01_rb,9.876490e-01_rb,9.873784e-01_rb,&
        & 9.871081e-01_rb /)
      ssaice3(:, 23) = (/ &
! band 23
        & 9.999343e-01_rb,9.998917e-01_rb,9.998492e-01_rb,9.998067e-01_rb,9.997642e-01_rb,&
        & 9.997218e-01_rb,9.996795e-01_rb,9.996372e-01_rb,9.995949e-01_rb,9.995528e-01_rb,&
        & 9.995106e-01_rb,9.994686e-01_rb,9.994265e-01_rb,9.993845e-01_rb,9.993426e-01_rb,&
        & 9.993007e-01_rb,9.992589e-01_rb,9.992171e-01_rb,9.991754e-01_rb,9.991337e-01_rb,&
        & 9.990921e-01_rb,9.990505e-01_rb,9.990089e-01_rb,9.989674e-01_rb,9.989260e-01_rb,&
        & 9.988846e-01_rb,9.988432e-01_rb,9.988019e-01_rb,9.987606e-01_rb,9.987194e-01_rb,&
        & 9.986782e-01_rb,9.986370e-01_rb,9.985959e-01_rb,9.985549e-01_rb,9.985139e-01_rb,&
        & 9.984729e-01_rb,9.984319e-01_rb,9.983910e-01_rb,9.983502e-01_rb,9.983094e-01_rb,&
        & 9.982686e-01_rb,9.982279e-01_rb,9.981872e-01_rb,9.981465e-01_rb,9.981059e-01_rb,&
        & 9.980653e-01_rb /)
      ssaice3(:, 24) = (/ &
! band 24
        & 9.999978e-01_rb,9.999965e-01_rb,9.999952e-01_rb,9.999939e-01_rb,9.999926e-01_rb,&
        & 9.999913e-01_rb,9.999900e-01_rb,9.999887e-01_rb,9.999873e-01_rb,9.999860e-01_rb,&
        & 9.999847e-01_rb,9.999834e-01_rb,9.999821e-01_rb,9.999808e-01_rb,9.999795e-01_rb,&
        & 9.999782e-01_rb,9.999769e-01_rb,9.999756e-01_rb,9.999743e-01_rb,9.999730e-01_rb,&
        & 9.999717e-01_rb,9.999704e-01_rb,9.999691e-01_rb,9.999678e-01_rb,9.999665e-01_rb,&
        & 9.999652e-01_rb,9.999639e-01_rb,9.999626e-01_rb,9.999613e-01_rb,9.999600e-01_rb,&
        & 9.999587e-01_rb,9.999574e-01_rb,9.999561e-01_rb,9.999548e-01_rb,9.999535e-01_rb,&
        & 9.999522e-01_rb,9.999509e-01_rb,9.999496e-01_rb,9.999483e-01_rb,9.999470e-01_rb,&
        & 9.999457e-01_rb,9.999444e-01_rb,9.999431e-01_rb,9.999418e-01_rb,9.999405e-01_rb,&
        & 9.999392e-01_rb /)
      ssaice3(:, 25) = (/ &
! band 25
        & 9.999994e-01_rb,9.999993e-01_rb,9.999991e-01_rb,9.999990e-01_rb,9.999989e-01_rb,&
        & 9.999987e-01_rb,9.999986e-01_rb,9.999984e-01_rb,9.999983e-01_rb,9.999982e-01_rb,&
        & 9.999980e-01_rb,9.999979e-01_rb,9.999977e-01_rb,9.999976e-01_rb,9.999975e-01_rb,&
        & 9.999973e-01_rb,9.999972e-01_rb,9.999970e-01_rb,9.999969e-01_rb,9.999967e-01_rb,&
        & 9.999966e-01_rb,9.999965e-01_rb,9.999963e-01_rb,9.999962e-01_rb,9.999960e-01_rb,&
        & 9.999959e-01_rb,9.999957e-01_rb,9.999956e-01_rb,9.999954e-01_rb,9.999953e-01_rb,&
        & 9.999952e-01_rb,9.999950e-01_rb,9.999949e-01_rb,9.999947e-01_rb,9.999946e-01_rb,&
        & 9.999944e-01_rb,9.999943e-01_rb,9.999941e-01_rb,9.999940e-01_rb,9.999939e-01_rb,&
        & 9.999937e-01_rb,9.999936e-01_rb,9.999934e-01_rb,9.999933e-01_rb,9.999931e-01_rb,&
        & 9.999930e-01_rb /)
      ssaice3(:, 26) = (/ &
! band 26
        & 9.999997e-01_rb,9.999995e-01_rb,9.999992e-01_rb,9.999990e-01_rb,9.999987e-01_rb,&
        & 9.999985e-01_rb,9.999983e-01_rb,9.999980e-01_rb,9.999978e-01_rb,9.999976e-01_rb,&
        & 9.999973e-01_rb,9.999971e-01_rb,9.999969e-01_rb,9.999967e-01_rb,9.999965e-01_rb,&
        & 9.999963e-01_rb,9.999960e-01_rb,9.999958e-01_rb,9.999956e-01_rb,9.999954e-01_rb,&
        & 9.999952e-01_rb,9.999950e-01_rb,9.999948e-01_rb,9.999946e-01_rb,9.999944e-01_rb,&
        & 9.999942e-01_rb,9.999939e-01_rb,9.999937e-01_rb,9.999935e-01_rb,9.999933e-01_rb,&
        & 9.999931e-01_rb,9.999929e-01_rb,9.999927e-01_rb,9.999925e-01_rb,9.999923e-01_rb,&
        & 9.999920e-01_rb,9.999918e-01_rb,9.999916e-01_rb,9.999914e-01_rb,9.999911e-01_rb,&
        & 9.999909e-01_rb,9.999907e-01_rb,9.999905e-01_rb,9.999902e-01_rb,9.999900e-01_rb,&
        & 9.999897e-01_rb /)
      ssaice3(:, 27) = (/ &
! band 27
        & 9.999991e-01_rb,9.999985e-01_rb,9.999980e-01_rb,9.999974e-01_rb,9.999968e-01_rb,&
        & 9.999963e-01_rb,9.999957e-01_rb,9.999951e-01_rb,9.999946e-01_rb,9.999940e-01_rb,&
        & 9.999934e-01_rb,9.999929e-01_rb,9.999923e-01_rb,9.999918e-01_rb,9.999912e-01_rb,&
        & 9.999907e-01_rb,9.999901e-01_rb,9.999896e-01_rb,9.999891e-01_rb,9.999885e-01_rb,&
        & 9.999880e-01_rb,9.999874e-01_rb,9.999869e-01_rb,9.999863e-01_rb,9.999858e-01_rb,&
        & 9.999853e-01_rb,9.999847e-01_rb,9.999842e-01_rb,9.999836e-01_rb,9.999831e-01_rb,&
        & 9.999826e-01_rb,9.999820e-01_rb,9.999815e-01_rb,9.999809e-01_rb,9.999804e-01_rb,&
        & 9.999798e-01_rb,9.999793e-01_rb,9.999787e-01_rb,9.999782e-01_rb,9.999776e-01_rb,&
        & 9.999770e-01_rb,9.999765e-01_rb,9.999759e-01_rb,9.999754e-01_rb,9.999748e-01_rb,&
        & 9.999742e-01_rb /)
      ssaice3(:, 28) = (/ &
! band 28
        & 9.999975e-01_rb,9.999961e-01_rb,9.999946e-01_rb,9.999931e-01_rb,9.999917e-01_rb,&
        & 9.999903e-01_rb,9.999888e-01_rb,9.999874e-01_rb,9.999859e-01_rb,9.999845e-01_rb,&
        & 9.999831e-01_rb,9.999816e-01_rb,9.999802e-01_rb,9.999788e-01_rb,9.999774e-01_rb,&
        & 9.999759e-01_rb,9.999745e-01_rb,9.999731e-01_rb,9.999717e-01_rb,9.999702e-01_rb,&
        & 9.999688e-01_rb,9.999674e-01_rb,9.999660e-01_rb,9.999646e-01_rb,9.999631e-01_rb,&
        & 9.999617e-01_rb,9.999603e-01_rb,9.999589e-01_rb,9.999574e-01_rb,9.999560e-01_rb,&
        & 9.999546e-01_rb,9.999532e-01_rb,9.999517e-01_rb,9.999503e-01_rb,9.999489e-01_rb,&
        & 9.999474e-01_rb,9.999460e-01_rb,9.999446e-01_rb,9.999431e-01_rb,9.999417e-01_rb,&
        & 9.999403e-01_rb,9.999388e-01_rb,9.999374e-01_rb,9.999359e-01_rb,9.999345e-01_rb,&
        & 9.999330e-01_rb /)
      ssaice3(:, 29) = (/ &
! band 29
        & 4.526500e-01_rb,5.287890e-01_rb,5.410487e-01_rb,5.459865e-01_rb,5.485149e-01_rb,&
        & 5.498914e-01_rb,5.505895e-01_rb,5.508310e-01_rb,5.507364e-01_rb,5.503793e-01_rb,&
        & 5.498090e-01_rb,5.490612e-01_rb,5.481637e-01_rb,5.471395e-01_rb,5.460083e-01_rb,&
        & 5.447878e-01_rb,5.434946e-01_rb,5.421442e-01_rb,5.407514e-01_rb,5.393309e-01_rb,&
        & 5.378970e-01_rb,5.364641e-01_rb,5.350464e-01_rb,5.336582e-01_rb,5.323140e-01_rb,&
        & 5.310283e-01_rb,5.298158e-01_rb,5.286914e-01_rb,5.276704e-01_rb,5.267680e-01_rb,&
        & 5.260000e-01_rb,5.253823e-01_rb,5.249311e-01_rb,5.246629e-01_rb,5.245946e-01_rb,&
        & 5.247434e-01_rb,5.251268e-01_rb,5.257626e-01_rb,5.266693e-01_rb,5.278653e-01_rb,&
        & 5.293698e-01_rb,5.312022e-01_rb,5.333823e-01_rb,5.359305e-01_rb,5.388676e-01_rb,&
        & 5.422146e-01_rb /)

! asymmetry factor: unitless
      asyice3(:, 16) = (/ &
! band 16
        & 8.340752e-01_rb,8.435170e-01_rb,8.517487e-01_rb,8.592064e-01_rb,8.660387e-01_rb,&
        & 8.723204e-01_rb,8.780997e-01_rb,8.834137e-01_rb,8.882934e-01_rb,8.927662e-01_rb,&
        & 8.968577e-01_rb,9.005914e-01_rb,9.039899e-01_rb,9.070745e-01_rb,9.098659e-01_rb,&
        & 9.123836e-01_rb,9.146466e-01_rb,9.166734e-01_rb,9.184817e-01_rb,9.200886e-01_rb,&
        & 9.215109e-01_rb,9.227648e-01_rb,9.238661e-01_rb,9.248304e-01_rb,9.256727e-01_rb,&
        & 9.264078e-01_rb,9.270505e-01_rb,9.276150e-01_rb,9.281156e-01_rb,9.285662e-01_rb,&
        & 9.289806e-01_rb,9.293726e-01_rb,9.297557e-01_rb,9.301435e-01_rb,9.305491e-01_rb,&
        & 9.309859e-01_rb,9.314671e-01_rb,9.320055e-01_rb,9.326140e-01_rb,9.333053e-01_rb,&
        & 9.340919e-01_rb,9.349861e-01_rb,9.360000e-01_rb,9.371451e-01_rb,9.384329e-01_rb,&
        & 9.398744e-01_rb /)
      asyice3(:, 17) = (/ &
! band 17
        & 8.728160e-01_rb,8.777333e-01_rb,8.823754e-01_rb,8.867535e-01_rb,8.908785e-01_rb,&
        & 8.947611e-01_rb,8.984118e-01_rb,9.018408e-01_rb,9.050582e-01_rb,9.080739e-01_rb,&
        & 9.108976e-01_rb,9.135388e-01_rb,9.160068e-01_rb,9.183106e-01_rb,9.204595e-01_rb,&
        & 9.224620e-01_rb,9.243271e-01_rb,9.260632e-01_rb,9.276788e-01_rb,9.291822e-01_rb,&
        & 9.305817e-01_rb,9.318853e-01_rb,9.331012e-01_rb,9.342372e-01_rb,9.353013e-01_rb,&
        & 9.363013e-01_rb,9.372450e-01_rb,9.381400e-01_rb,9.389939e-01_rb,9.398145e-01_rb,&
        & 9.406092e-01_rb,9.413856e-01_rb,9.421511e-01_rb,9.429131e-01_rb,9.436790e-01_rb,&
        & 9.444561e-01_rb,9.452517e-01_rb,9.460729e-01_rb,9.469270e-01_rb,9.478209e-01_rb,&
        & 9.487617e-01_rb,9.497562e-01_rb,9.508112e-01_rb,9.519335e-01_rb,9.531294e-01_rb,&
        & 9.544055e-01_rb /)
      asyice3(:, 18) = (/ &
! band 18
        & 7.897566e-01_rb,7.948704e-01_rb,7.998041e-01_rb,8.045623e-01_rb,8.091495e-01_rb,&
        & 8.135702e-01_rb,8.178290e-01_rb,8.219305e-01_rb,8.258790e-01_rb,8.296792e-01_rb,&
        & 8.333355e-01_rb,8.368524e-01_rb,8.402343e-01_rb,8.434856e-01_rb,8.466108e-01_rb,&
        & 8.496143e-01_rb,8.525004e-01_rb,8.552737e-01_rb,8.579384e-01_rb,8.604990e-01_rb,&
        & 8.629597e-01_rb,8.653250e-01_rb,8.675992e-01_rb,8.697867e-01_rb,8.718916e-01_rb,&
        & 8.739185e-01_rb,8.758715e-01_rb,8.777551e-01_rb,8.795734e-01_rb,8.813308e-01_rb,&
        & 8.830315e-01_rb,8.846799e-01_rb,8.862802e-01_rb,8.878366e-01_rb,8.893534e-01_rb,&
        & 8.908350e-01_rb,8.922854e-01_rb,8.937090e-01_rb,8.951099e-01_rb,8.964925e-01_rb,&
        & 8.978609e-01_rb,8.992192e-01_rb,9.005718e-01_rb,9.019229e-01_rb,9.032765e-01_rb,&
        & 9.046369e-01_rb /)
      asyice3(:, 19) = (/ &
! band 19
        & 7.812615e-01_rb,7.887764e-01_rb,7.959664e-01_rb,8.028413e-01_rb,8.094109e-01_rb,&
        & 8.156849e-01_rb,8.216730e-01_rb,8.273846e-01_rb,8.328294e-01_rb,8.380166e-01_rb,&
        & 8.429556e-01_rb,8.476556e-01_rb,8.521258e-01_rb,8.563753e-01_rb,8.604131e-01_rb,&
        & 8.642481e-01_rb,8.678893e-01_rb,8.713455e-01_rb,8.746254e-01_rb,8.777378e-01_rb,&
        & 8.806914e-01_rb,8.834948e-01_rb,8.861566e-01_rb,8.886854e-01_rb,8.910897e-01_rb,&
        & 8.933779e-01_rb,8.955586e-01_rb,8.976402e-01_rb,8.996311e-01_rb,9.015398e-01_rb,&
        & 9.033745e-01_rb,9.051436e-01_rb,9.068555e-01_rb,9.085185e-01_rb,9.101410e-01_rb,&
        & 9.117311e-01_rb,9.132972e-01_rb,9.148476e-01_rb,9.163905e-01_rb,9.179340e-01_rb,&
        & 9.194864e-01_rb,9.210559e-01_rb,9.226505e-01_rb,9.242784e-01_rb,9.259476e-01_rb,&
        & 9.276661e-01_rb /)
      asyice3(:, 20) = (/ &
! band 20
        & 7.640720e-01_rb,7.691119e-01_rb,7.739941e-01_rb,7.787222e-01_rb,7.832998e-01_rb,&
        & 7.877304e-01_rb,7.920177e-01_rb,7.961652e-01_rb,8.001765e-01_rb,8.040551e-01_rb,&
        & 8.078044e-01_rb,8.114280e-01_rb,8.149294e-01_rb,8.183119e-01_rb,8.215791e-01_rb,&
        & 8.247344e-01_rb,8.277812e-01_rb,8.307229e-01_rb,8.335629e-01_rb,8.363046e-01_rb,&
        & 8.389514e-01_rb,8.415067e-01_rb,8.439738e-01_rb,8.463560e-01_rb,8.486568e-01_rb,&
        & 8.508795e-01_rb,8.530274e-01_rb,8.551039e-01_rb,8.571122e-01_rb,8.590558e-01_rb,&
        & 8.609378e-01_rb,8.627618e-01_rb,8.645309e-01_rb,8.662485e-01_rb,8.679178e-01_rb,&
        & 8.695423e-01_rb,8.711251e-01_rb,8.726697e-01_rb,8.741792e-01_rb,8.756571e-01_rb,&
        & 8.771065e-01_rb,8.785307e-01_rb,8.799331e-01_rb,8.813169e-01_rb,8.826854e-01_rb,&
        & 8.840419e-01_rb /)
      asyice3(:, 21) = (/ &
! band 21
        & 7.602598e-01_rb,7.651572e-01_rb,7.699014e-01_rb,7.744962e-01_rb,7.789452e-01_rb,&
        & 7.832522e-01_rb,7.874205e-01_rb,7.914538e-01_rb,7.953555e-01_rb,7.991290e-01_rb,&
        & 8.027777e-01_rb,8.063049e-01_rb,8.097140e-01_rb,8.130081e-01_rb,8.161906e-01_rb,&
        & 8.192645e-01_rb,8.222331e-01_rb,8.250993e-01_rb,8.278664e-01_rb,8.305374e-01_rb,&
        & 8.331153e-01_rb,8.356030e-01_rb,8.380037e-01_rb,8.403201e-01_rb,8.425553e-01_rb,&
        & 8.447121e-01_rb,8.467935e-01_rb,8.488022e-01_rb,8.507412e-01_rb,8.526132e-01_rb,&
        & 8.544210e-01_rb,8.561675e-01_rb,8.578554e-01_rb,8.594875e-01_rb,8.610665e-01_rb,&
        & 8.625951e-01_rb,8.640760e-01_rb,8.655119e-01_rb,8.669055e-01_rb,8.682594e-01_rb,&
        & 8.695763e-01_rb,8.708587e-01_rb,8.721094e-01_rb,8.733308e-01_rb,8.745255e-01_rb,&
        & 8.756961e-01_rb /)
      asyice3(:, 22) = (/ &
! band 22
        & 7.568957e-01_rb,7.606995e-01_rb,7.644072e-01_rb,7.680204e-01_rb,7.715402e-01_rb,&
        & 7.749682e-01_rb,7.783057e-01_rb,7.815541e-01_rb,7.847148e-01_rb,7.877892e-01_rb,&
        & 7.907786e-01_rb,7.936846e-01_rb,7.965084e-01_rb,7.992515e-01_rb,8.019153e-01_rb,&
        & 8.045011e-01_rb,8.070103e-01_rb,8.094444e-01_rb,8.118048e-01_rb,8.140927e-01_rb,&
        & 8.163097e-01_rb,8.184571e-01_rb,8.205364e-01_rb,8.225488e-01_rb,8.244958e-01_rb,&
        & 8.263789e-01_rb,8.281993e-01_rb,8.299586e-01_rb,8.316580e-01_rb,8.332991e-01_rb,&
        & 8.348831e-01_rb,8.364115e-01_rb,8.378857e-01_rb,8.393071e-01_rb,8.406770e-01_rb,&
        & 8.419969e-01_rb,8.432682e-01_rb,8.444923e-01_rb,8.456706e-01_rb,8.468044e-01_rb,&
        & 8.478952e-01_rb,8.489444e-01_rb,8.499533e-01_rb,8.509234e-01_rb,8.518561e-01_rb,&
        & 8.527528e-01_rb /)
      asyice3(:, 23) = (/ &
! band 23
        & 7.575066e-01_rb,7.606912e-01_rb,7.638236e-01_rb,7.669035e-01_rb,7.699306e-01_rb,&
        & 7.729046e-01_rb,7.758254e-01_rb,7.786926e-01_rb,7.815060e-01_rb,7.842654e-01_rb,&
        & 7.869705e-01_rb,7.896211e-01_rb,7.922168e-01_rb,7.947574e-01_rb,7.972428e-01_rb,&
        & 7.996726e-01_rb,8.020466e-01_rb,8.043646e-01_rb,8.066262e-01_rb,8.088313e-01_rb,&
        & 8.109796e-01_rb,8.130709e-01_rb,8.151049e-01_rb,8.170814e-01_rb,8.190001e-01_rb,&
        & 8.208608e-01_rb,8.226632e-01_rb,8.244071e-01_rb,8.260924e-01_rb,8.277186e-01_rb,&
        & 8.292856e-01_rb,8.307932e-01_rb,8.322411e-01_rb,8.336291e-01_rb,8.349570e-01_rb,&
        & 8.362244e-01_rb,8.374312e-01_rb,8.385772e-01_rb,8.396621e-01_rb,8.406856e-01_rb,&
        & 8.416476e-01_rb,8.425479e-01_rb,8.433861e-01_rb,8.441620e-01_rb,8.448755e-01_rb,&
        & 8.455263e-01_rb /)
      asyice3(:, 24) = (/ &
! band 24
        & 7.568829e-01_rb,7.597947e-01_rb,7.626745e-01_rb,7.655212e-01_rb,7.683337e-01_rb,&
        & 7.711111e-01_rb,7.738523e-01_rb,7.765565e-01_rb,7.792225e-01_rb,7.818494e-01_rb,&
        & 7.844362e-01_rb,7.869819e-01_rb,7.894854e-01_rb,7.919459e-01_rb,7.943623e-01_rb,&
        & 7.967337e-01_rb,7.990590e-01_rb,8.013373e-01_rb,8.035676e-01_rb,8.057488e-01_rb,&
        & 8.078802e-01_rb,8.099605e-01_rb,8.119890e-01_rb,8.139645e-01_rb,8.158862e-01_rb,&
        & 8.177530e-01_rb,8.195641e-01_rb,8.213183e-01_rb,8.230149e-01_rb,8.246527e-01_rb,&
        & 8.262308e-01_rb,8.277483e-01_rb,8.292042e-01_rb,8.305976e-01_rb,8.319275e-01_rb,&
        & 8.331929e-01_rb,8.343929e-01_rb,8.355265e-01_rb,8.365928e-01_rb,8.375909e-01_rb,&
        & 8.385197e-01_rb,8.393784e-01_rb,8.401659e-01_rb,8.408815e-01_rb,8.415240e-01_rb,&
        & 8.420926e-01_rb /)
      asyice3(:, 25) = (/ &
! band 25
        & 7.548616e-01_rb,7.575454e-01_rb,7.602153e-01_rb,7.628696e-01_rb,7.655067e-01_rb,&
        & 7.681249e-01_rb,7.707225e-01_rb,7.732978e-01_rb,7.758492e-01_rb,7.783750e-01_rb,&
        & 7.808735e-01_rb,7.833430e-01_rb,7.857819e-01_rb,7.881886e-01_rb,7.905612e-01_rb,&
        & 7.928983e-01_rb,7.951980e-01_rb,7.974588e-01_rb,7.996789e-01_rb,8.018567e-01_rb,&
        & 8.039905e-01_rb,8.060787e-01_rb,8.081196e-01_rb,8.101115e-01_rb,8.120527e-01_rb,&
        & 8.139416e-01_rb,8.157764e-01_rb,8.175557e-01_rb,8.192776e-01_rb,8.209405e-01_rb,&
        & 8.225427e-01_rb,8.240826e-01_rb,8.255585e-01_rb,8.269688e-01_rb,8.283117e-01_rb,&
        & 8.295856e-01_rb,8.307889e-01_rb,8.319198e-01_rb,8.329767e-01_rb,8.339579e-01_rb,&
        & 8.348619e-01_rb,8.356868e-01_rb,8.364311e-01_rb,8.370930e-01_rb,8.376710e-01_rb,&
        & 8.381633e-01_rb /)
      asyice3(:, 26) = (/ &
! band 26
        & 7.491854e-01_rb,7.518523e-01_rb,7.545089e-01_rb,7.571534e-01_rb,7.597839e-01_rb,&
        & 7.623987e-01_rb,7.649959e-01_rb,7.675737e-01_rb,7.701303e-01_rb,7.726639e-01_rb,&
        & 7.751727e-01_rb,7.776548e-01_rb,7.801084e-01_rb,7.825318e-01_rb,7.849230e-01_rb,&
        & 7.872804e-01_rb,7.896020e-01_rb,7.918862e-01_rb,7.941309e-01_rb,7.963345e-01_rb,&
        & 7.984951e-01_rb,8.006109e-01_rb,8.026802e-01_rb,8.047009e-01_rb,8.066715e-01_rb,&
        & 8.085900e-01_rb,8.104546e-01_rb,8.122636e-01_rb,8.140150e-01_rb,8.157072e-01_rb,&
        & 8.173382e-01_rb,8.189063e-01_rb,8.204096e-01_rb,8.218464e-01_rb,8.232148e-01_rb,&
        & 8.245130e-01_rb,8.257391e-01_rb,8.268915e-01_rb,8.279682e-01_rb,8.289675e-01_rb,&
        & 8.298875e-01_rb,8.307264e-01_rb,8.314824e-01_rb,8.321537e-01_rb,8.327385e-01_rb,&
        & 8.332350e-01_rb /)
      asyice3(:, 27) = (/ &
! band 27
        & 7.397086e-01_rb,7.424069e-01_rb,7.450955e-01_rb,7.477725e-01_rb,7.504362e-01_rb,&
        & 7.530846e-01_rb,7.557159e-01_rb,7.583283e-01_rb,7.609199e-01_rb,7.634888e-01_rb,&
        & 7.660332e-01_rb,7.685512e-01_rb,7.710411e-01_rb,7.735009e-01_rb,7.759288e-01_rb,&
        & 7.783229e-01_rb,7.806814e-01_rb,7.830024e-01_rb,7.852841e-01_rb,7.875246e-01_rb,&
        & 7.897221e-01_rb,7.918748e-01_rb,7.939807e-01_rb,7.960380e-01_rb,7.980449e-01_rb,&
        & 7.999995e-01_rb,8.019000e-01_rb,8.037445e-01_rb,8.055311e-01_rb,8.072581e-01_rb,&
        & 8.089235e-01_rb,8.105255e-01_rb,8.120623e-01_rb,8.135319e-01_rb,8.149326e-01_rb,&
        & 8.162626e-01_rb,8.175198e-01_rb,8.187025e-01_rb,8.198089e-01_rb,8.208371e-01_rb,&
        & 8.217852e-01_rb,8.226514e-01_rb,8.234338e-01_rb,8.241306e-01_rb,8.247399e-01_rb,&
        & 8.252599e-01_rb /)
      asyice3(:, 28) = (/ &
! band 28
        & 7.224533e-01_rb,7.251681e-01_rb,7.278728e-01_rb,7.305654e-01_rb,7.332444e-01_rb,&
        & 7.359078e-01_rb,7.385539e-01_rb,7.411808e-01_rb,7.437869e-01_rb,7.463702e-01_rb,&
        & 7.489291e-01_rb,7.514616e-01_rb,7.539661e-01_rb,7.564408e-01_rb,7.588837e-01_rb,&
        & 7.612933e-01_rb,7.636676e-01_rb,7.660049e-01_rb,7.683034e-01_rb,7.705612e-01_rb,&
        & 7.727767e-01_rb,7.749480e-01_rb,7.770733e-01_rb,7.791509e-01_rb,7.811789e-01_rb,&
        & 7.831556e-01_rb,7.850791e-01_rb,7.869478e-01_rb,7.887597e-01_rb,7.905131e-01_rb,&
        & 7.922062e-01_rb,7.938372e-01_rb,7.954044e-01_rb,7.969059e-01_rb,7.983399e-01_rb,&
        & 7.997047e-01_rb,8.009985e-01_rb,8.022195e-01_rb,8.033658e-01_rb,8.044357e-01_rb,&
        & 8.054275e-01_rb,8.063392e-01_rb,8.071692e-01_rb,8.079157e-01_rb,8.085768e-01_rb,&
        & 8.091507e-01_rb /)
      asyice3(:, 29) = (/ &
! band 29
        & 8.850026e-01_rb,9.005489e-01_rb,9.069242e-01_rb,9.121799e-01_rb,9.168987e-01_rb,&
        & 9.212259e-01_rb,9.252176e-01_rb,9.289028e-01_rb,9.323000e-01_rb,9.354235e-01_rb,&
        & 9.382858e-01_rb,9.408985e-01_rb,9.432734e-01_rb,9.454218e-01_rb,9.473557e-01_rb,&
        & 9.490871e-01_rb,9.506282e-01_rb,9.519917e-01_rb,9.531904e-01_rb,9.542374e-01_rb,&
        & 9.551461e-01_rb,9.559298e-01_rb,9.566023e-01_rb,9.571775e-01_rb,9.576692e-01_rb,&
        & 9.580916e-01_rb,9.584589e-01_rb,9.587853e-01_rb,9.590851e-01_rb,9.593729e-01_rb,&
        & 9.596632e-01_rb,9.599705e-01_rb,9.603096e-01_rb,9.606954e-01_rb,9.611427e-01_rb,&
        & 9.616667e-01_rb,9.622826e-01_rb,9.630060e-01_rb,9.638524e-01_rb,9.648379e-01_rb,&
        & 9.659788e-01_rb,9.672916e-01_rb,9.687933e-01_rb,9.705014e-01_rb,9.724337e-01_rb,&
        & 9.746084e-01_rb /)

! fdelta: unitless
      fdlice3(:, 16) = (/ &
! band 16
        & 4.959277e-02_rb,4.685292e-02_rb,4.426104e-02_rb,4.181231e-02_rb,3.950191e-02_rb,&
        & 3.732500e-02_rb,3.527675e-02_rb,3.335235e-02_rb,3.154697e-02_rb,2.985578e-02_rb,&
        & 2.827395e-02_rb,2.679666e-02_rb,2.541909e-02_rb,2.413640e-02_rb,2.294378e-02_rb,&
        & 2.183639e-02_rb,2.080940e-02_rb,1.985801e-02_rb,1.897736e-02_rb,1.816265e-02_rb,&
        & 1.740905e-02_rb,1.671172e-02_rb,1.606585e-02_rb,1.546661e-02_rb,1.490917e-02_rb,&
        & 1.438870e-02_rb,1.390038e-02_rb,1.343939e-02_rb,1.300089e-02_rb,1.258006e-02_rb,&
        & 1.217208e-02_rb,1.177212e-02_rb,1.137536e-02_rb,1.097696e-02_rb,1.057210e-02_rb,&
        & 1.015596e-02_rb,9.723704e-03_rb,9.270516e-03_rb,8.791565e-03_rb,8.282026e-03_rb,&
        & 7.737072e-03_rb,7.151879e-03_rb,6.521619e-03_rb,5.841467e-03_rb,5.106597e-03_rb,&
        & 4.312183e-03_rb /)
      fdlice3(:, 17) = (/ &
! band 17
        & 5.071224e-02_rb,5.000217e-02_rb,4.933872e-02_rb,4.871992e-02_rb,4.814380e-02_rb,&
        & 4.760839e-02_rb,4.711170e-02_rb,4.665177e-02_rb,4.622662e-02_rb,4.583426e-02_rb,&
        & 4.547274e-02_rb,4.514007e-02_rb,4.483428e-02_rb,4.455340e-02_rb,4.429544e-02_rb,&
        & 4.405844e-02_rb,4.384041e-02_rb,4.363939e-02_rb,4.345340e-02_rb,4.328047e-02_rb,&
        & 4.311861e-02_rb,4.296586e-02_rb,4.282024e-02_rb,4.267977e-02_rb,4.254248e-02_rb,&
        & 4.240640e-02_rb,4.226955e-02_rb,4.212995e-02_rb,4.198564e-02_rb,4.183462e-02_rb,&
        & 4.167494e-02_rb,4.150462e-02_rb,4.132167e-02_rb,4.112413e-02_rb,4.091003e-02_rb,&
        & 4.067737e-02_rb,4.042420e-02_rb,4.014854e-02_rb,3.984840e-02_rb,3.952183e-02_rb,&
        & 3.916683e-02_rb,3.878144e-02_rb,3.836368e-02_rb,3.791158e-02_rb,3.742316e-02_rb,&
        & 3.689645e-02_rb /)
      fdlice3(:, 18) = (/ &
! band 18
        & 1.062938e-01_rb,1.065234e-01_rb,1.067822e-01_rb,1.070682e-01_rb,1.073793e-01_rb,&
        & 1.077137e-01_rb,1.080693e-01_rb,1.084442e-01_rb,1.088364e-01_rb,1.092439e-01_rb,&
        & 1.096647e-01_rb,1.100970e-01_rb,1.105387e-01_rb,1.109878e-01_rb,1.114423e-01_rb,&
        & 1.119004e-01_rb,1.123599e-01_rb,1.128190e-01_rb,1.132757e-01_rb,1.137279e-01_rb,&
        & 1.141738e-01_rb,1.146113e-01_rb,1.150385e-01_rb,1.154534e-01_rb,1.158540e-01_rb,&
        & 1.162383e-01_rb,1.166045e-01_rb,1.169504e-01_rb,1.172741e-01_rb,1.175738e-01_rb,&
        & 1.178472e-01_rb,1.180926e-01_rb,1.183080e-01_rb,1.184913e-01_rb,1.186405e-01_rb,&
        & 1.187538e-01_rb,1.188291e-01_rb,1.188645e-01_rb,1.188580e-01_rb,1.188076e-01_rb,&
        & 1.187113e-01_rb,1.185672e-01_rb,1.183733e-01_rb,1.181277e-01_rb,1.178282e-01_rb,&
        & 1.174731e-01_rb /)
      fdlice3(:, 19) = (/ &
! band 19
        & 1.076195e-01_rb,1.065195e-01_rb,1.054696e-01_rb,1.044673e-01_rb,1.035099e-01_rb,&
        & 1.025951e-01_rb,1.017203e-01_rb,1.008831e-01_rb,1.000808e-01_rb,9.931116e-02_rb,&
        & 9.857151e-02_rb,9.785939e-02_rb,9.717230e-02_rb,9.650774e-02_rb,9.586322e-02_rb,&
        & 9.523623e-02_rb,9.462427e-02_rb,9.402484e-02_rb,9.343544e-02_rb,9.285358e-02_rb,&
        & 9.227675e-02_rb,9.170245e-02_rb,9.112818e-02_rb,9.055144e-02_rb,8.996974e-02_rb,&
        & 8.938056e-02_rb,8.878142e-02_rb,8.816981e-02_rb,8.754323e-02_rb,8.689919e-02_rb,&
        & 8.623517e-02_rb,8.554869e-02_rb,8.483724e-02_rb,8.409832e-02_rb,8.332943e-02_rb,&
        & 8.252807e-02_rb,8.169175e-02_rb,8.081795e-02_rb,7.990419e-02_rb,7.894796e-02_rb,&
        & 7.794676e-02_rb,7.689809e-02_rb,7.579945e-02_rb,7.464834e-02_rb,7.344227e-02_rb,&
        & 7.217872e-02_rb /)
      fdlice3(:, 20) = (/ &
! band 20
        & 1.119014e-01_rb,1.122706e-01_rb,1.126690e-01_rb,1.130947e-01_rb,1.135456e-01_rb,&
        & 1.140199e-01_rb,1.145154e-01_rb,1.150302e-01_rb,1.155623e-01_rb,1.161096e-01_rb,&
        & 1.166703e-01_rb,1.172422e-01_rb,1.178233e-01_rb,1.184118e-01_rb,1.190055e-01_rb,&
        & 1.196025e-01_rb,1.202008e-01_rb,1.207983e-01_rb,1.213931e-01_rb,1.219832e-01_rb,&
        & 1.225665e-01_rb,1.231411e-01_rb,1.237050e-01_rb,1.242561e-01_rb,1.247926e-01_rb,&
        & 1.253122e-01_rb,1.258132e-01_rb,1.262934e-01_rb,1.267509e-01_rb,1.271836e-01_rb,&
        & 1.275896e-01_rb,1.279669e-01_rb,1.283134e-01_rb,1.286272e-01_rb,1.289063e-01_rb,&
        & 1.291486e-01_rb,1.293522e-01_rb,1.295150e-01_rb,1.296351e-01_rb,1.297104e-01_rb,&
        & 1.297390e-01_rb,1.297189e-01_rb,1.296480e-01_rb,1.295244e-01_rb,1.293460e-01_rb,&
        & 1.291109e-01_rb /)
      fdlice3(:, 21) = (/ &
! band 21
        & 1.133298e-01_rb,1.136777e-01_rb,1.140556e-01_rb,1.144615e-01_rb,1.148934e-01_rb,&
        & 1.153492e-01_rb,1.158269e-01_rb,1.163243e-01_rb,1.168396e-01_rb,1.173706e-01_rb,&
        & 1.179152e-01_rb,1.184715e-01_rb,1.190374e-01_rb,1.196108e-01_rb,1.201897e-01_rb,&
        & 1.207720e-01_rb,1.213558e-01_rb,1.219389e-01_rb,1.225194e-01_rb,1.230951e-01_rb,&
        & 1.236640e-01_rb,1.242241e-01_rb,1.247733e-01_rb,1.253096e-01_rb,1.258309e-01_rb,&
        & 1.263352e-01_rb,1.268205e-01_rb,1.272847e-01_rb,1.277257e-01_rb,1.281415e-01_rb,&
        & 1.285300e-01_rb,1.288893e-01_rb,1.292173e-01_rb,1.295118e-01_rb,1.297710e-01_rb,&
        & 1.299927e-01_rb,1.301748e-01_rb,1.303154e-01_rb,1.304124e-01_rb,1.304637e-01_rb,&
        & 1.304673e-01_rb,1.304212e-01_rb,1.303233e-01_rb,1.301715e-01_rb,1.299638e-01_rb,&
        & 1.296983e-01_rb /)
      fdlice3(:, 22) = (/ &
! band 22
        & 1.145360e-01_rb,1.153256e-01_rb,1.161453e-01_rb,1.169929e-01_rb,1.178666e-01_rb,&
        & 1.187641e-01_rb,1.196835e-01_rb,1.206227e-01_rb,1.215796e-01_rb,1.225522e-01_rb,&
        & 1.235383e-01_rb,1.245361e-01_rb,1.255433e-01_rb,1.265579e-01_rb,1.275779e-01_rb,&
        & 1.286011e-01_rb,1.296257e-01_rb,1.306494e-01_rb,1.316703e-01_rb,1.326862e-01_rb,&
        & 1.336951e-01_rb,1.346950e-01_rb,1.356838e-01_rb,1.366594e-01_rb,1.376198e-01_rb,&
        & 1.385629e-01_rb,1.394866e-01_rb,1.403889e-01_rb,1.412678e-01_rb,1.421212e-01_rb,&
        & 1.429469e-01_rb,1.437430e-01_rb,1.445074e-01_rb,1.452381e-01_rb,1.459329e-01_rb,&
        & 1.465899e-01_rb,1.472069e-01_rb,1.477819e-01_rb,1.483128e-01_rb,1.487976e-01_rb,&
        & 1.492343e-01_rb,1.496207e-01_rb,1.499548e-01_rb,1.502346e-01_rb,1.504579e-01_rb,&
        & 1.506227e-01_rb /)
      fdlice3(:, 23) = (/ &
! band 23
        & 1.153263e-01_rb,1.161445e-01_rb,1.169932e-01_rb,1.178703e-01_rb,1.187738e-01_rb,&
        & 1.197016e-01_rb,1.206516e-01_rb,1.216217e-01_rb,1.226099e-01_rb,1.236141e-01_rb,&
        & 1.246322e-01_rb,1.256621e-01_rb,1.267017e-01_rb,1.277491e-01_rb,1.288020e-01_rb,&
        & 1.298584e-01_rb,1.309163e-01_rb,1.319736e-01_rb,1.330281e-01_rb,1.340778e-01_rb,&
        & 1.351207e-01_rb,1.361546e-01_rb,1.371775e-01_rb,1.381873e-01_rb,1.391820e-01_rb,&
        & 1.401593e-01_rb,1.411174e-01_rb,1.420540e-01_rb,1.429671e-01_rb,1.438547e-01_rb,&
        & 1.447146e-01_rb,1.455449e-01_rb,1.463433e-01_rb,1.471078e-01_rb,1.478364e-01_rb,&
        & 1.485270e-01_rb,1.491774e-01_rb,1.497857e-01_rb,1.503497e-01_rb,1.508674e-01_rb,&
        & 1.513367e-01_rb,1.517554e-01_rb,1.521216e-01_rb,1.524332e-01_rb,1.526880e-01_rb,&
        & 1.528840e-01_rb /)
      fdlice3(:, 24) = (/ &
! band 24
        & 1.160842e-01_rb,1.169118e-01_rb,1.177697e-01_rb,1.186556e-01_rb,1.195676e-01_rb,&
        & 1.205036e-01_rb,1.214616e-01_rb,1.224394e-01_rb,1.234349e-01_rb,1.244463e-01_rb,&
        & 1.254712e-01_rb,1.265078e-01_rb,1.275539e-01_rb,1.286075e-01_rb,1.296664e-01_rb,&
        & 1.307287e-01_rb,1.317923e-01_rb,1.328550e-01_rb,1.339149e-01_rb,1.349699e-01_rb,&
        & 1.360179e-01_rb,1.370567e-01_rb,1.380845e-01_rb,1.390991e-01_rb,1.400984e-01_rb,&
        & 1.410803e-01_rb,1.420429e-01_rb,1.429840e-01_rb,1.439016e-01_rb,1.447936e-01_rb,&
        & 1.456579e-01_rb,1.464925e-01_rb,1.472953e-01_rb,1.480642e-01_rb,1.487972e-01_rb,&
        & 1.494923e-01_rb,1.501472e-01_rb,1.507601e-01_rb,1.513287e-01_rb,1.518511e-01_rb,&
        & 1.523252e-01_rb,1.527489e-01_rb,1.531201e-01_rb,1.534368e-01_rb,1.536969e-01_rb,&
        & 1.538984e-01_rb /)
      fdlice3(:, 25) = (/ &
! band 25
        & 1.168725e-01_rb,1.177088e-01_rb,1.185747e-01_rb,1.194680e-01_rb,1.203867e-01_rb,&
        & 1.213288e-01_rb,1.222923e-01_rb,1.232750e-01_rb,1.242750e-01_rb,1.252903e-01_rb,&
        & 1.263187e-01_rb,1.273583e-01_rb,1.284069e-01_rb,1.294626e-01_rb,1.305233e-01_rb,&
        & 1.315870e-01_rb,1.326517e-01_rb,1.337152e-01_rb,1.347756e-01_rb,1.358308e-01_rb,&
        & 1.368788e-01_rb,1.379175e-01_rb,1.389449e-01_rb,1.399590e-01_rb,1.409577e-01_rb,&
        & 1.419389e-01_rb,1.429007e-01_rb,1.438410e-01_rb,1.447577e-01_rb,1.456488e-01_rb,&
        & 1.465123e-01_rb,1.473461e-01_rb,1.481483e-01_rb,1.489166e-01_rb,1.496492e-01_rb,&
        & 1.503439e-01_rb,1.509988e-01_rb,1.516118e-01_rb,1.521808e-01_rb,1.527038e-01_rb,&
        & 1.531788e-01_rb,1.536037e-01_rb,1.539764e-01_rb,1.542951e-01_rb,1.545575e-01_rb,&
        & 1.547617e-01_rb /)
      fdlice3(:, 26) = (/ &
!band 26
        & 1.180509e-01_rb,1.189025e-01_rb,1.197820e-01_rb,1.206875e-01_rb,1.216171e-01_rb,&
        & 1.225687e-01_rb,1.235404e-01_rb,1.245303e-01_rb,1.255363e-01_rb,1.265564e-01_rb,&
        & 1.275888e-01_rb,1.286313e-01_rb,1.296821e-01_rb,1.307392e-01_rb,1.318006e-01_rb,&
        & 1.328643e-01_rb,1.339284e-01_rb,1.349908e-01_rb,1.360497e-01_rb,1.371029e-01_rb,&
        & 1.381486e-01_rb,1.391848e-01_rb,1.402095e-01_rb,1.412208e-01_rb,1.422165e-01_rb,&
        & 1.431949e-01_rb,1.441539e-01_rb,1.450915e-01_rb,1.460058e-01_rb,1.468947e-01_rb,&
        & 1.477564e-01_rb,1.485888e-01_rb,1.493900e-01_rb,1.501580e-01_rb,1.508907e-01_rb,&
        & 1.515864e-01_rb,1.522428e-01_rb,1.528582e-01_rb,1.534305e-01_rb,1.539578e-01_rb,&
        & 1.544380e-01_rb,1.548692e-01_rb,1.552494e-01_rb,1.555767e-01_rb,1.558490e-01_rb,&
        & 1.560645e-01_rb /)
      fdlice3(:, 27) = (/ &
! band 27
        & 1.200480e-01_rb,1.209267e-01_rb,1.218304e-01_rb,1.227575e-01_rb,1.237059e-01_rb,&
        & 1.246739e-01_rb,1.256595e-01_rb,1.266610e-01_rb,1.276765e-01_rb,1.287041e-01_rb,&
        & 1.297420e-01_rb,1.307883e-01_rb,1.318412e-01_rb,1.328988e-01_rb,1.339593e-01_rb,&
        & 1.350207e-01_rb,1.360813e-01_rb,1.371393e-01_rb,1.381926e-01_rb,1.392396e-01_rb,&
        & 1.402783e-01_rb,1.413069e-01_rb,1.423235e-01_rb,1.433263e-01_rb,1.443134e-01_rb,&
        & 1.452830e-01_rb,1.462332e-01_rb,1.471622e-01_rb,1.480681e-01_rb,1.489490e-01_rb,&
        & 1.498032e-01_rb,1.506286e-01_rb,1.514236e-01_rb,1.521863e-01_rb,1.529147e-01_rb,&
        & 1.536070e-01_rb,1.542614e-01_rb,1.548761e-01_rb,1.554491e-01_rb,1.559787e-01_rb,&
        & 1.564629e-01_rb,1.568999e-01_rb,1.572879e-01_rb,1.576249e-01_rb,1.579093e-01_rb,&
        & 1.581390e-01_rb /)
      fdlice3(:, 28) = (/ &
! band 28
        & 1.247813e-01_rb,1.256496e-01_rb,1.265417e-01_rb,1.274560e-01_rb,1.283905e-01_rb,&
        & 1.293436e-01_rb,1.303135e-01_rb,1.312983e-01_rb,1.322964e-01_rb,1.333060e-01_rb,&
        & 1.343252e-01_rb,1.353523e-01_rb,1.363855e-01_rb,1.374231e-01_rb,1.384632e-01_rb,&
        & 1.395042e-01_rb,1.405441e-01_rb,1.415813e-01_rb,1.426140e-01_rb,1.436404e-01_rb,&
        & 1.446587e-01_rb,1.456672e-01_rb,1.466640e-01_rb,1.476475e-01_rb,1.486157e-01_rb,&
        & 1.495671e-01_rb,1.504997e-01_rb,1.514117e-01_rb,1.523016e-01_rb,1.531673e-01_rb,&
        & 1.540073e-01_rb,1.548197e-01_rb,1.556026e-01_rb,1.563545e-01_rb,1.570734e-01_rb,&
        & 1.577576e-01_rb,1.584054e-01_rb,1.590149e-01_rb,1.595843e-01_rb,1.601120e-01_rb,&
        & 1.605962e-01_rb,1.610349e-01_rb,1.614266e-01_rb,1.617693e-01_rb,1.620614e-01_rb,&
        & 1.623011e-01_rb /)
      fdlice3(:, 29) = (/ &
! band 29
        & 1.006055e-01_rb,9.549582e-02_rb,9.063960e-02_rb,8.602900e-02_rb,8.165612e-02_rb,&
        & 7.751308e-02_rb,7.359199e-02_rb,6.988496e-02_rb,6.638412e-02_rb,6.308156e-02_rb,&
        & 5.996942e-02_rb,5.703979e-02_rb,5.428481e-02_rb,5.169657e-02_rb,4.926719e-02_rb,&
        & 4.698880e-02_rb,4.485349e-02_rb,4.285339e-02_rb,4.098061e-02_rb,3.922727e-02_rb,&
        & 3.758547e-02_rb,3.604733e-02_rb,3.460497e-02_rb,3.325051e-02_rb,3.197604e-02_rb,&
        & 3.077369e-02_rb,2.963558e-02_rb,2.855381e-02_rb,2.752050e-02_rb,2.652776e-02_rb,&
        & 2.556772e-02_rb,2.463247e-02_rb,2.371415e-02_rb,2.280485e-02_rb,2.189670e-02_rb,&
        & 2.098180e-02_rb,2.005228e-02_rb,1.910024e-02_rb,1.811781e-02_rb,1.709709e-02_rb,&
        & 1.603020e-02_rb,1.490925e-02_rb,1.372635e-02_rb,1.247363e-02_rb,1.114319e-02_rb,&
        & 9.727157e-03_rb /)

      end subroutine swcldpr

      end module rrtmg_sw_init
