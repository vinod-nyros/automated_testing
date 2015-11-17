from obdjects.templates import get_source_fname, CoffeescriptTemplate  # is_newer,

#print is_newer(__file__, __file__)

print get_source_fname (source='aha - this is a parm')

print get_source_fname ('aha - this is a parm')


my_cs_tester = CoffeescriptTemplate ('''\
        console.log "calling refresh"

        $.ajax '/utils/refresh',
            type: 'GET'
            timeout: 60000000
            dataType: 'html'
            error: (jqXHR, textStatus, errorThrown) ->
                console.log "AJAX Error!: #{textStatus}"
                console.log setTimeout("console.log('reloading...');location.reload(true)", 2000)
                console.log "After setTimeout!"
            success: (data, textStatus, jqXHR) ->
                console.log "Successful AJAX call: #{data}"
        ''',
        destination = 'mytest.js'
    )
