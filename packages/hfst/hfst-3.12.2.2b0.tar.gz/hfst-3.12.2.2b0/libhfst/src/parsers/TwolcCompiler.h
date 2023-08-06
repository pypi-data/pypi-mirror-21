//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, version 3 of the Licence.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with this program.  If not, see <http://www.gnu.org/licenses/>.

//#include "commandline_src/CommandLine.h"
//#include "HfstTwolcDefs.h"
//#include "io_src/InputReader.h"
//#include "grammar_defs.h"
//#include "rule_src/TwolCGrammar.h"
//#include "rule_src/OtherSymbolTransducer.h"

namespace hfst {

  class TwolcCompiler
  {
  private:
    CommandLine command_line;
    std::ostream & warning_stream;
    std::ostream & error_stream;
  public:
    TwolcCompiler(const CommandLine & cl, std::ostream & warn, std::ostream & error);
    void compile();
    void store(hfst::HfstOutputStream & ostr);
  };

}
