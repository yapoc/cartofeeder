#!/usr/bin/env python
# vi: set foldmethod=indent: set tabstop=2: set shiftwidth=2:
import argparse
import re
import whois
import time
import logging

LOG_LEVEL = logging.DEBUG
NB_MAX_TRY = 5
SLEEP_TIME = 10

def set_logger ():
    log_format = logging.Formatter ("[%(asctime)s] - %(levelname)-8s - %(name)-15s - %(message)s")
    handler = logging.StreamHandler ()
    handler.setLevel (LOG_LEVEL)
    handler.setFormatter (log_format)

    logger = logging.getLogger ("alimentation_carto")
    logger.setLevel (LOG_LEVEL)
    logger.addHandler (handler)
    
    return logger


def load_domains_from_file (input_file):
    domain_match = re.compile (r".*\..*")
    with open (input_file, 'r') as f:
        for l in f:
            m = re.match (domain_match, l)
            if m:
                l = l.strip ()
                yield l

def _do_whois (domain, nb_done = 0):
    while nb_done < NB_MAX_TRY:
        nb_done += 1
        try:
            return whois.query (domain)
        except Exception as e:
            logger.info ("Exception {}".format (e))
            if 'Too many requests' in str (e):
                sleep_delay = SLEEP_TIME * nb_done
                logger.info ("On attend {} sec et on relance!".format (sleep_delay))
                time.sleep (sleep_delay)
                return _do_whois (domain, nb_done)
            else:
                raise Exception ("Problème {}".format (e))


def get_n_parse_whois_for_domain (domain):
    result = {
        'registrar': '',
        'owner': '', 
        'exp_date': '', 
        'ns': ""
    }
    data = {}
    try:
        data = _do_whois (domain)
        result['registrar'] = data.registrar
        if data.expiration_date:
            result['exp_date'] = str (data.expiration_date).split (' ')[0] # ça, c'est dégueulasse...
        result['owner'] = data.registrant
        result['ns'] = ','.join (data.name_servers)
    except Exception as e:
        logger.error ("{} (génériq) -> Erreur {}".format (domain, e))
        logger.debug (data.__dict__)
        raise  Exception (e)
    return result

logger = set_logger ()

if __name__ == "__main__":
    parser = argparse.ArgumentParser ()
    parser.add_argument ('-i', '--input_file', help = 'Fichier contenant la liste des noms de domaine à requêter.', type = str, required = True)
    parser.add_argument ('-o', '--output_file', help = 'Fichier de rapport.', type = str, default = '/dev/stdout')
    args = parser.parse_args ()
    with open (args.output_file, 'w') as f:
        f.write ("""Domaine;Registrar;Propriétaire;Date Expiration;DNS\n""")
        for domain in load_domains_from_file (args.input_file):
            logger.info ("Traitement du domaine {}".format (domain))
            d = get_n_parse_whois_for_domain (domain)
            line_content = "{};{};{};{};{}\n".format (domain, d['registrar'], d['owner'], d['exp_date'], d['ns'])
            f.write (line_content)
            logger.debug ("Identification de {}".format (line_content))
            time.sleep (1)
