# Third-party notices

The root 0BSD license applies to the original Change Lens work and project-owned example content. It does not replace the licenses of third-party material.

## Phoenix scaffold in the examples

The GroupStay snapshots include source generated from Phoenix templates, including application scaffolding, configuration, web modules, and test support. Those portions retain the Phoenix MIT terms below. Application-specific benchmark requirements, implementation, and review content are released here under 0BSD to the extent held by the project publisher. The MIT notice also applies to corresponding embedded source and diff excerpts in `public/evidence/bundle.json`.

Source: https://github.com/phoenixframework/phoenix

The following notice is reproduced from the Phoenix dependency used in the captured review:

# MIT License

Copyright (c) 2014 Chris McCord

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Installed dependencies

Dependency source/build directories are not vendored. `package-lock.json` pins the UI dependency graph; each example's `mix.lock` pins its optional Elixir dependency graph. Installing or distributing these components retains their own license obligations.

The primary UI packages are React, React DOM, Vite, and the Vite React plugin (MIT). The npm lockfile also records transitive packages under Apache-2.0, ISC, BSD-3-Clause, and CC-BY-4.0, among others. Those dependency declarations are an inventory, not a grant to relicense them as 0BSD. Preserve the relevant notices when distributing a built application or a dependency.

The example configuration contains Phoenix-generated development/test signing keys for the fictional local service. They are not production credentials or keys used by Change Lens. Production configuration reads its secret from the environment.
