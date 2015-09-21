# == Define: ciwatch::initd_service
#
# Creates initd service for an executable which can not run as daemon and
# runs it in the python virtualenv.

define ciwatch::initd_service(
  $exec_cmd,
  $short_description,
  $runas_user,
  $service_name = $title,
) {

  ::ciwatch::log_wrapper{ "/usr/local/bin/${service_name}":
    exec_cmd => $exec_cmd,
    logbase  => $service_name,
  }

  # Template uses:
  # service_name
  # short_description
  # runas_user
  file { "/etc/init.d/${service_name}":
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0555',
    content => template('ciwatch/ciwatch_service.init.erb'),
  }

  service { $service_name:
    enable     => true,
    hasrestart => true,
    require    => File["/etc/init.d/${service_name}"],
  }

}