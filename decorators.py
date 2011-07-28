# Copyright (c) 2011, Jimmy Cao
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from oyoyo.parse import parse_nick
import botconfig

def generate(fdict, **kwargs):
    """Generates a decorator generator.  Always use this"""
    def cmd(*s, raw_nick=False, admin_only=False, owner_only=False):
        def dec(f):
            def innerf(*args):
                largs = list(args)
                if largs[1]:
                    cloak = parse_nick(largs[1])[3]
                else:
                    cloak = ""
                if not raw_nick and largs[1]:
                    largs[1] = parse_nick(largs[1])[0]  # username
                    #if largs[1].startswith("#"):       
                if owner_only:
                    if cloak and cloak in botconfig.OWNERS:
                        return f(*largs)
                    elif cloak:
                        largs[0].notice(largs[1], "You are not the owner.")
                        return
                if admin_only:
                    if cloak and (cloak in botconfig.ADMINS or cloak == botconfig.OWNER):
                        return f(*largs)
                    elif cloak:
                        largs[0].notice(largs[1], "You are not an admin.")
                        return
                return f(*largs)
            for x in s:
                if x not in fdict.keys():
                    fdict[x] = []
                else:
                    for fn in fdict[x]:
                        if (fn.owner_only != owner_only or
                            fn.admin_only != admin_only):
                            raise Exception("Command: "+x+" has non-matching protection levels!")
                fdict[x].append(innerf)
            innerf.owner_only = owner_only
            innerf.raw_nick = raw_nick
            innerf.admin_only = admin_only
            innerf.__doc__ = f.__doc__
            return innerf
            
        return dec
        
    return lambda *args, **kwarargs: cmd(*args, **kwarargs) if kwarargs else cmd(*args, **kwargs)