# Copyright (c) 2015, DjaoDjin inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from rest_framework.mixins import DestroyModelMixin
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from ..models import RelationShip
from ..serializers import RelationShipSerializer

class RelationShipListAPIView(DestroyModelMixin, generics.ListCreateAPIView):

    model = RelationShip
    serializer_class = RelationShipSerializer
    queryset = RelationShip.objects.all()

    def delete(self, request, *args, **kwargs):#pylint: disable=unused-argument
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        elements = self.queryset.filter(
            orig_element__slug__in=serializer.validated_data['orig_elements'],
            dest_element__slug__in=serializer.validated_data['dest_elements'])
        elements.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
