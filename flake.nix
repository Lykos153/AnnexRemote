{
  description = "Flake to setup python virtualenv with direnv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: 
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in rec {
      packages = rec {
        pythonEnv = pkgs.python3.withPackages(
          ps: with ps; [
            virtualenv
          ]
        );
        annexremote = pkgs.python3Packages.buildPythonPackage rec {
          pname = "annexremote";
          version = self.rev;
          format = "pyproject";
          src = self;
        };
        default = annexremote;
      };

      defaultPackage = packages.default;
      devShell = packages.pythonEnv.env;
    });
}
