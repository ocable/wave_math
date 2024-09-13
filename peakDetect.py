def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    
    """
    min_indexes = []
    min_values = []
    max_indexes = []
    max_values = []
       
    if x is None:
        x = range(len(v))
    
    mn, mx = float('inf'), -float('inf')
    mnpos, mxpos = float('nan'), float('nan')
    
    lookformax = True
    
    for i in range(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                max_indexes.append(mxpos)
                max_values.append(mx)
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                min_indexes.append(mnpos)
                min_values.append(mn)
                mx = this
                mxpos = x[i]
                lookformax = True

    return min_indexes, min_values, max_indexes, max_values