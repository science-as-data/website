using Franklin

cd(@__DIR__) do
    success = optimize(; prepath=get(ENV, "FRANKLIN_PREPATH", ""),
                        prerender=false, minify=false, sig=true, clear=true,
                        suppress_errors=false, fail_on_warning=true)
    success === true || error("Franklin website build failed")
end
