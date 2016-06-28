# python
import clipc_combine_process
import serve_netcdf

url1 = 'example/vDTR_JUN_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'

url2 = 'example/vDTR_OCT_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'

nc_combo , url_combo = clipc_combine_process.combine_two_indecies(url1, url2, "*")
#nc_combo , url_combo = clipc_combine_process.combine_two_indecies(url1, url2, "+")

serve_netcdf.visualise(url1, url2, url_combo)

