--[[
  This script will set the s.mod value of all zones in your instrument to MAX or
  the total length of each zone. 
  One option though, in case you want only to target groups with a certain substring,
  change the value of GROUP_NAME_SUB_STRING to your desired substring present in
  the names of the groups you want to process their zones. Otherwise, set it to an
  empty string as "".
]]--

local kt = Kontakt

INSTRUMENT_IDX = 0

local GROUP_NAME_SUB_STRING = "| LOOPS"

for z = 0, kt.get_num_zones(0)-1 do
    local zone_group_index = kt.get_zone_group(INSTRUMENT_IDX, z)
    local group_name = kt.get_group_name(INSTRUMENT_IDX, zone_group_index)
    local is_loop, _ = string.find(group_name, GROUP_NAME_SUB_STRING)

    if is_loop then
        local zone_length = kt.get_zone_sample_frames(INSTRUMENT_IDX, z)
        kt.set_zone_sample_start_mod_range(INSTRUMENT_IDX, z, zone_length)
    end
    
end
