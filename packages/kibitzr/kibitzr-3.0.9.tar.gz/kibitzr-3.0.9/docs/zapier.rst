.. _zapier:

==================================================
How to hook Kibitzr notification to Zapier trigger
==================================================

`Kibitzr <https://kibitzr.github.io/>`__ is perfect for scrapping deep
web, and it is even better when combined with integration solutions for
the public web. One of the most popular integration platforms is
`Zapier <https://zapier.com/>`__. It has a free plan, that should cover
personal needs.

If you don't have Kibitzr installed, it's a good time to get one with
`AWS Free Tier <https://kibitzr.readthedocs.io/en/latest/aws.html>`__ or
`GCP Always Free <https://kibitzr.readthedocs.io/en/latest/gcp.html>`__
instance.

This tutorial will guide through a creation of basic Kibitzr check wired
to Zapier trigger.

1. Create new zap - click **MAKE A ZAP!** button on
   `Zapier dashboard <https://zapier.com/app/dashboard>`__.

2. For a trigger app choose **Webhooks** > **Catch Hook**.

3. Leave *Child Key* empty.

4. Copy hook URL.

5. Add a check to ``kibitzr.yml``:

   .. code-block:: yaml

    checks:
      - name: Kibitzr release
        url: https://pypi.python.org/pypi/kibitzr/json
        transform:
          - jq: .info | .version
          - changes: verbose
        notify:
          - zapier: https://hooks.zapier.com/hooks/catch/1628105/1kan4u/

   (Replace with you zapier URL).

6.  Launch kibitzr::

    kibitzr

7.  Make sure Trigger test passes.

8.  Add Zapier action. Let's pick something fancy like SMS.

9.  Enter your phone number, verify code if needed.

10. In message template choose **Step 1 > Text** from drop-down list.

You're all set! Get notified on the new version of Kibitzr through SMS.
