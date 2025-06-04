-- This is intended to be used in Creator Tools

-- in case the group scanned contains the substring, all its zones will have their smod set to max
function set_smod_to_max_on_specific_groups(name_sub_string)
    for g = 0, #instrument.groups-1 do
        for z = 0, #instrument.groups[g].zones-1 do
            local g_name = instrument.groups[g].name
            -- in case you need a verification depending on the name of the group
            local is_loop, _ = string.find(g_name, name_sub_string, 1, true)
            if is_loop ~= nil then
                instrument.groups[g].zones[z].sampleStartModRange = instrument.groups[g].zones[z].sampleEnd
            end
        end
    end
end

function set_all_zones_smod_to_max()
    for g = 0, #instrument.groups-1 do
        for z = 0, #instrument.groups[g].zones-1 do
            instrument.groups[g].zones[z].sampleStartModRange = instrument.groups[g].zones[z].sampleEnd
        end
    end
end
