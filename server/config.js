const fs = require('fs')
const { getAbsolutePath } = require("./utils");

const ensurePathExists = (p) => {
  if (!fs.existsSync(p)) {
    console.log("ERROR. Path", p, "doesn't exist.");
    process.exit(1);
  }
}

const parseConfig = (args) => {
  let config = JSON.parse(fs.readFileSync(getAbsolutePath(args.config)));

  /* check config file has the appropriate fields... */

  /* sort out paths */
  config.referenceConfigPath = getAbsolutePath(config.referenceConfigPath);
  config.referencePanelPath = getAbsolutePath(config.referencePanelPath);
  config.basecalledPath = getAbsolutePath(config.basecalledPath);
  config.demuxedPath = getAbsolutePath(config.demuxedPath);

  /* check if paths exist (perhaps we could make them if they don't) */
  ensurePathExists(config.referenceConfigPath);
  ensurePathExists(config.referencePanelPath);
  ensurePathExists(config.basecalledPath);
  ensurePathExists(config.demuxedPath);

  /* parse the "main reference" configuration file (e.g. primers, genes, ref seq etc) */
  const secondConfig = JSON.parse(fs.readFileSync(config.referenceConfigPath));
  config = {...config, ...secondConfig};

  /* get the names of the sequences in the reference panel */
  config.referencePanel = fs.readFileSync(config.referencePanelPath, "utf8")
    .split("\n")
    .filter((l) => l.startsWith(">"))
    .map((n) => n.substring(1)); // remove the > character

  return config;
}

module.exports = {
  parseConfig
};